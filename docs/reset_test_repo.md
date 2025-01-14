# Test repo Reset Workflow

## Intention

For easier development a [dedicated testing repository](https://github.com/ynput/ayon-addon-action-testing/) was created.
Since applying more and more action changes onto a repository would quickly lead to issues even in RnD the next step was to implement this automated reset workflow.

## Overview

* Verify secrets
* Remove existing repo
* Create new repo based on [addon-template](https://github.com/ynput/ayon-addon-template)
* Add on workflow user as repo admin
* Set all kinds of properties for the repo (description, topic, variables, labels)
* Add templates and workflows
* Automatically create initial release
* Create dummy-PRs for testing

## Benefits

* Enables consistent testing environment
* Always the same starting point
* Automatically tests the initial release trigger - and therefore some parts fo the release trigger too
* Could be extended to build automated integration tests
* Parts of it could be used for a repo creation workflow
