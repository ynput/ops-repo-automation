## Known issue for [testing environment](https://github.com/ynput/ayon-addon-action-testing)

* package.py wont create any additional files in this repo
* Therefore no changes happen in this step and no commit
* Version tag gets set one commit behind

## Docs notes

* Document repo reset workflow

* Add basic troubleshooting instructions especially towards github-query action
* Explain visible output in runs and how to interpret it

* Explain intended workflow limitation
  * From github
    * Org secrets not available to workflow runs started by Prs from forks
    * Workflow nesting limitations
    * Type conversions and how most data will be interpreted as strings
    * dispatch_workflow converts all inputs to strings
    * [from_json](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#operators) can be used to convert strings to numbers or boolean

* Document important todos
  * Full integration testing still missing
  * Describe how to approach it
  * How to build repo creation workflow from repo reset workflow
  * Add testing workflow for PRs from forks

## Development notes

* Add tag to hash verification to release workflow
