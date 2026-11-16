"""Shared MkDocs hooks for the API docs of AYON repositories.

- Add temporary `__init__.py` files to Python folders that miss one, so
  `mkdocs-autoapi` doesn't skip them, and remove them after the build.
- Remove `__pycache__` folders before the build.
- Options a repository can set under `extra` in its `mkdocs.yml`:
  - `private: true` hides the repository link and the source code of
    documented objects, for private repositories.
  - `document_root_files: true` documents the Python files in the
    repository root, which are ignored by default.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

from mkdocs.plugins import event_priority

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig

# Top level folders scanned for Python packages that miss `__init__.py`.
# Folders that don't exist in a repository are skipped.
SCAN_ROOTS = ("client", "server", "services", "service", "common")

log = logging.getLogger("mkdocs.hooks.ayon")

_created_init_files: list[Path] = []


def _is_hidden(path: Path, root: Path) -> bool:
    return any(
        part.startswith(".") for part in path.relative_to(root).parts
    )


def add_missing_init_files(roots: tuple[str, ...]) -> None:
    """Add `__init__.py` to every folder with Python files that misses one.

    Parent folders up to and including the root get one too, so the whole
    package path is importable.
    """
    for root in roots:
        root_path = Path(root).resolve()
        if not root_path.is_dir():
            continue
        for dirpath, _, files in os.walk(root_path):
            path = Path(dirpath)
            if "__init__.py" in files or _is_hidden(path, root_path):
                continue
            if not any(name.endswith(".py") for name in files):
                continue
            while True:
                init_file = path / "__init__.py"
                if init_file.exists():
                    break
                init_file.touch()
                _created_init_files.append(init_file)
                log.info("Created temporary '%s'", init_file)
                if path == root_path:
                    break
                path = path.parent


def remove_missing_init_files() -> None:
    """Remove the `__init__.py` files added by `add_missing_init_files`."""
    while _created_init_files:
        init_file = _created_init_files.pop()
        init_file.unlink(missing_ok=True)
        log.info("Removed temporary '%s'", init_file)


def remove_pycache_dirs() -> None:
    """Remove all `__pycache__` folders in the repository."""
    for dirpath, dirs, _ in os.walk("."):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
            rmtree(Path(dirpath, "__pycache__"))


# mkdocs hooks ----------------------------------------------------------------


# Run before the plugins read their options.
@event_priority(100)
def on_config(config: MkDocsConfig) -> MkDocsConfig:
    if config.extra.get("private", False):
        # Drop the repository link even if `repo_url` was set by mistake.
        config.repo_url = None
        config.repo_name = None
        config.edit_uri = None
        handlers = config.plugins["mkdocstrings"].config.handlers
        python_handler = handlers.setdefault("python", {})
        python_handler.setdefault("options", {})["show_source"] = False
        log.info("Private repository: repository link and source code hidden")

    if config.extra.get("document_root_files", False):
        autoapi_ignore = (
            config.plugins["mkdocs-autoapi"].config.autoapi_ignore
        )
        autoapi_ignore[:] = [
            pattern for pattern in autoapi_ignore if pattern != "./*.py"
        ]
        log.info("Python files in the repository root are documented")
    return config


def on_startup(*, command: str, dirty: bool) -> None:
    remove_pycache_dirs()


def on_pre_build(config: MkDocsConfig) -> None:
    try:
        add_missing_init_files(SCAN_ROOTS)
    except BaseException:
        remove_missing_init_files()
        raise


def on_post_build(config: MkDocsConfig) -> None:
    remove_missing_init_files()


def on_build_error(error: Exception) -> None:
    remove_missing_init_files()
