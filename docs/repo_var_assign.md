# Assign Repository Variable

Batch assign repository variables

## Intention

Assign new repository variables to a bunch of repositories at once can be q pretty annoying task so this workflow is supposed to take care of it.

## Features

* Loop over comma separated value string of ynput owned repository names
* Skip repo if name was not found and output warning
* Skip over repo if variable already exists (and no overwrite options set)
* Overwrite existing variables in case they already exist

## Usage

Run manually from actions page of [ops-repo-automation](https://github.com/ynput/ops-repo-automation)
Provide inputs:

* Variable name (will be set to all caps no matter the input casing)
* Variable value to assign
* Repository names as comma separated string - comma (",") and comma space (", ") will work here
* Optional overwrite - in case existing values need to be replaced
