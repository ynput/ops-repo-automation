## Known issue for [testing environment](https://github.com/ynput/ayon-addon-action-testing)

* package.py wont create any additional files in this repo
* Therefore no changes happen in this step and no commit
* Version tag gets set one commit behind

## Docs notes

* Document repo reset workflow
* Document push workflows like caller push_caller_workflow and assign_repo_var
* Explain concepts uf reusability amongst existing workflows

* Add basic troubleshooting instructions especially towards github-query action
* Explain visible output in runs and how to interpret it

* Document important todos
  * Full integration testing still missing
  * Describe how to approach it
  * How to build repo creation workflow from repo reset workflow

## Development notes

* Add tag to hash verification to release workflow
