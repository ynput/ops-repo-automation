# Ops Repo Automation

Collection of templates, automation tools and github-workflows for Ayon related repositories.

## Terminology

* Github Workflow - usually a .yml file which defines all steps to be run automatically
* GitHub Action - stand-alone workflow module which works like a function using input parameters, processes internal logic and returns results
* Caller Workflow - usually a pretty short .yml file which just calls larger workflows
* Missing point

## Development Repository Structure

### Main Workflow [Repository](https://github.com/ynput/ops-repo-automation)

This is intended to be the centralized workflow location which can be called from caller workflows in others repositories.
The main workflows should be stored in .github/workflows to be accessible for caller workflows.

In caller_workflows you will find templates for caller workflows which are ready to be implemented in other repositories.

the branch_rules directory currently holds some exported rule sets for main and develop branch to be applied during repo creation.

### Ephermal Testing [Repository](https://github.com/ynput/ayon-addon-action-testing)

This repository is effected by every run of the reset_test_repo workflow. It's intended as pure testing repository to mimic different repository states with any manual setup needed.

In the long run this should get extended to allow fully automated integration testing with an actual repository to make sure any kind of workflow change doesn't actually break any expected results.

### Action Repositories

These should be dedicated github actions custom implemented and maintained by input to allow full control.
These are supposed to handle standalone functional parts of the workflow logic to be easy to use.

They are also supposed to include there own unit-tests to verify they do work as expected and any changes don't break critical logic.
They can be implemented in either raw bash scripts, python code as seen in [Github-Query](https://github.com/ynput/github-query) or as a docker.

Right now only one exists but there are more to come.

* [Github-Query](https://github.com/ynput/github-query)

### Implementation Rules

The baseline of a workflow should be implemented in pure bash commands since this is the default in workflows anyway.
These workflows should then be stored in .github/workflows of this [repository]((https://github.com/ynput/ayon-addon-action-testing))

Further any more complex logic like data conversion, formatting of api results or similar should be grouped into logical units and implemented as a github action.

This should lead to (relatively) short workflows with low visible complexity. Which are easy to read in the end.
