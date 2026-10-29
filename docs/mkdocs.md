# Shared MkDocs setup

The API docs of AYON repositories (`docs.ayon.dev/<repo>/`) are built by
`deploy_mkdocs.yml` and `deploy_mkdocs_remote_repo.yml`. The toolchain they
use is kept in one place, the [`mkdocs/`](../mkdocs) folder of this repository:

| File | Purpose |
|---|---|
| `mkdocs/base.yml` | Shared MkDocs config: theme, markdown extensions, plugins, hooks |
| `mkdocs/hooks.py` | Shared MkDocs hooks: temporary `__init__.py` files for autoapi, `__pycache__` cleanup, the options below |
| `mkdocs/requirements.txt` | Shared Python requirements |
| `mkdocs/overrides/` | Shared assets: logo, favicon, `css/custom.css` |
| `mkdocs/cleanup_versions.py` | Deletes old deployed versions, run by the workflows after `mike deploy` |

The workflows check `mkdocs/` out to `.docs-setup/` inside the repository being
built, install `.docs-setup/mkdocs/requirements.txt` on a pinned Python version
and then run `mike deploy`.

## Repository setup

A repository keeps only its own `mkdocs.yml` and its `docs/` folder with the
content (`index.md`, `license.md`, ...):

```yaml
INHERIT: .docs-setup/mkdocs/base.yml
site_name: ayon-houdini
repo_url: https://github.com/ynput/ayon-houdini
nav:
  - Home: index.md
  - License: license.md
```

Add `.docs-setup/` to the repository's `.gitignore`. `mkdocs_hooks.py`,
`mkdocs_requirements.txt`, `docs/css/` and `docs/img/` are not needed anymore.

### Options

The shared setup exposes these options under `extra` in `mkdocs.yml`:

```yaml
extra:
  private: true              # default: false
  document_root_files: true  # default: false
  versions_to_keep: 15       # default: keep all versions
```

- `private: true` is for private repositories. It hides the repository link
  in the header, even when `repo_url` is set, and the source code of
  documented objects. Docstrings and signatures are still published, so
  check them for links to the private repository.
- `document_root_files: true` documents the Python files in the repository
  root (e.g. `start.py` in `ayon-launcher`), which are ignored by default.
- `versions_to_keep: <n>` deletes all but the newest `n` versions from
  `gh-pages` after each deploy (`mkdocs/cleanup_versions.py`). Versions are
  ordered by version number, not by deploy date. The `test-build` version
  is never counted or deleted by it.

### Repository specific additions

Use these only when a repository really needs something the shared setup
doesn't have; anything useful to more repositories belongs in `mkdocs/`.

- **Requirements:** add them to `mkdocs/requirements.txt`, even if only one
  repository uses them, so all repositories build with the same packages.
- **Hooks:** add the repository's own hook file after the shared one. The
  `hooks` list replaces the shared one, so the shared hooks must be listed too:
  ```yaml
  hooks:
    - .docs-setup/mkdocs/hooks.py
    - mkdocs_hooks.py
  ```
- **Assets:** a file in `docs/` with the same path as one in
  `mkdocs/overrides/` (e.g. `docs/img/favicon.ico`) replaces it.

Keys in `mkdocs.yml` override the same keys in `base.yml`. Dictionaries such as
`theme` and `extra` are merged, but lists are replaced as a whole: setting
`plugins`, `markdown_extensions` or `theme.features` means repeating the full
list from `base.yml`.

Repositories that don't inherit from `base.yml` yet still build with their own
`mkdocs.yml`, `mkdocs_hooks.py` and `mkdocs_requirements.txt`; the workflows
install that file together with the shared requirements only for them. Delete
it when switching a repository to the shared setup.

## Building locally

From the repository root:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/ynput/ops-repo-automation.git .docs-setup
git -C .docs-setup sparse-checkout set mkdocs
pip install -r .docs-setup/mkdocs/requirements.txt
mkdocs serve
```

Update the shared setup with `git -C .docs-setup pull`.

## Testing changes to the shared setup

The `docs_setup_ref` input picks the ref of this repository the shared setup
is taken from (default `develop`). To test a branch, point the caller workflow
to it for both the workflow and the setup:

```yaml
jobs:
  build-mk-docs:
    uses: ynput/ops-repo-automation/.github/workflows/deploy_mkdocs.yml@<branch>
    with:
      repo: ${{ github.repository }}
      docs_setup_ref: <branch>
```
