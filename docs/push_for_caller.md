# Workflow to push caller workflows

Update/push caller workflows to many repos at once.

## Intention

Updating the caller workflows manually isn't an option, therefore we need a way to update these caller workflows at scale.

## Features

* Loop over ynput repositories having a provided topic assigned
* Skip over workflow file if it already exists (and no overwrite options set)
* Overwrite existing workflow files in case they already exist
* Dry Run option to check what repo would get a change and which won't without actually applying changes

## Usage

Run manually from actions page of [ops-repo-automation](https://github.com/ynput/ops-repo-automation)
Provide inputs:

* variable_name (will be set to all caps no matter the input casing)
* Caller Workflow name to push
* repo_topic
* Optional overwrite - in case existing workflows need to be replaced
* dry_run yes/no
