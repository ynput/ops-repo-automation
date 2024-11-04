#!/usr/bin/env python
import os
from typing import Optional, List, Dict, Any

import requests

YNPUT_CLOUD_URL: Optional[str] = os.getenv("YNPUT_CLOUD_URL")
YNPUT_CLOUD_TOKEN: Optional[str] = os.getenv("YNPUT_CLOUD_TOKEN")
OUTPUT_DIR: Optional[str] = os.getenv("OUTPUT_DIR")


def update_addon_metadata(addon_name: str, metadata: Dict[str, Any]):
    headers = {
        "x-api-key": YNPUT_CLOUD_TOKEN
    }

    res = requests.put(
        f"{YNPUT_CLOUD_URL}/addons/{addon_name}",
        headers=headers,
        json=metadata,
    )
    res.raise_for_status()


def upload_addon_package(addon_name: str, filepath: str):
    headers = {
        "x-api-key": YNPUT_CLOUD_TOKEN
    }
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as stream:
        res = requests.put(
            f"{YNPUT_CLOUD_URL}/addons/{addon_name}/{filename}",
            headers=headers,
            data=stream
        )
    res.raise_for_status()


def _filter_addon_package_filename(
    filenames: List[str],
    addon_name: str,
    addon_version: str
):
    if len(filenames) == 1:
        return filenames[0]

    print(
        "Multiple files found in OUTPUT_DIR, trying"
        " to filter them by addon name and version."
    )
    best_name = f"{addon_name}-{addon_version}.zip"
    if best_name in filenames:
        return best_name

    filtered_filenames = [
        filename
        for filename in filenames
        if filename.endswith(".zip") and filename.startswith(addon_name)
    ]
    if len(filtered_filenames) > 1:
        filtered_filenames = [
            filename
            for filename in filtered_filenames
            if addon_version in  filename
        ]

    if not filtered_filenames:
        raise ValueError("No valid files found in OUTPUT_DIR")

    if len(filtered_filenames) == 1:
        return filtered_filenames[0]

    raise ValueError(
        "Multiple files in OUTPUT_DIR match expected filename criteria."
    )


def main():
    if not YNPUT_CLOUD_URL:
        raise ValueError("YNPUT_CLOUD_URL environment variable is not set")

    if not YNPUT_CLOUD_TOKEN:
        raise ValueError("YNPUT_CLOUD_TOKEN environment variable is not set")

    if not OUTPUT_DIR:
        raise ValueError("OUTPUT_DIR is not set.")

    if not os.path.exists(OUTPUT_DIR):
        raise ValueError("OUTPUT_DIR does not exist.")

    package_content = {}
    with open("package.py", "r") as stream:
        exec(stream.read(), package_content)
    addon_name = package_content["name"]
    addon_version = package_content["version"]

    filenames = list(os.listdir(OUTPUT_DIR))
    if not filenames:
        raise ValueError("No files found in OUTPUT_DIR")

    filename = _filter_addon_package_filename(
        filenames, addon_name, addon_version
    )
    filepath = os.path.join(OUTPUT_DIR, filename)
    upload_addon_package(addon_name, filepath)

    # TODO implement 'update_addon_metadata' function
    # - we need to define where to look for the metadata


if __name__ == "__main__":
    main()
