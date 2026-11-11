"""Delete old documentation versions deployed with mike.

Keeps the newest `extra.versions_to_keep` versions set in the repository's
`mkdocs.yml` and deletes the rest. Does nothing when the option isn't set.

Run it from the repository root after `mike deploy`; arguments are passed
to mike, e.g.:

    python cleanup_versions.py --branch gh-pages --push
"""
from __future__ import annotations

import json
import subprocess
import sys

from mkdocs.config import load_config

# Handled separately by the deploy workflows.
IGNORED_VERSIONS = {"test-build"}


def main(mike_args: list[str]) -> None:
    keep = load_config("mkdocs.yml").extra.get("versions_to_keep")
    if keep is None:
        print("'versions_to_keep' is not set, keeping all versions.")
        return
    if not isinstance(keep, int) or isinstance(keep, bool) or keep < 1:
        sys.exit(
            f"'versions_to_keep' must be a positive integer, got {keep!r}."
        )

    list_args = [arg for arg in mike_args if arg not in ("-p", "--push")]
    result = subprocess.run(
        ["mike", "list", "--json", *list_args],
        check=True,
        capture_output=True,
        text=True,
    )
    # mike lists the versions from the newest to the oldest.
    versions = [
        item["version"]
        for item in json.loads(result.stdout)
        if item["version"] not in IGNORED_VERSIONS
    ]
    old_versions = versions[keep:]
    if not old_versions:
        print(f"{len(versions)} versions deployed, nothing to delete.")
        return

    print(f"Keeping {versions[:keep]}")
    print(f"Deleting {old_versions}")
    subprocess.run(["mike", "delete", *old_versions, *mike_args], check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
