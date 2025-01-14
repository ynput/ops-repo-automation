# Assign Repository Variable

Batch assign repository variables

## Intention

Assign new repository variables to a bunch of repositories at once can be q pretty annoying task so this workflow is supposed to take care of it.

## Features

* Loop over ynput repositories having a provided topic assigned
* Skip over repo if variable already exists (and no overwrite options set)
* Overwrite existing variables in case they already exist
* Dry Run option to check what repo would get a change and which won't without actually applying changes

## Usage

Run manually from actions page of [ops-repo-automation](https://github.com/ynput/ops-repo-automation)
Provide inputs:

* variable_name (will be set to all caps no matter the input casing)
* variable_value to assign
* repo_topic
* Optional overwrite - in case existing values need to be replaced
* dry_run yes/no
