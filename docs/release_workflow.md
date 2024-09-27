# Intention

The Release Worflow is meant to have a one-click solution to handling all release related tasks.
This includes validation, merging branches, creating artifacts and so on.

## Structure

The workflow is split into multiple jobs, each handeling a different kind of logic.
Additionally the jobs run certain dedicated Github Actions which are stand-alone units
Some Examples in use right now (27.09.24)

### Ynput-Owned

* [GitHub-Query](https://github.com/ynput/github-query) - used for pull-re quest data collection

### Github-Owned

* [Checkout](https://github.com/actions/checkout) - checkout repository
* [Upload-Artifact](https://github.com/actions/upload-artifact) - Provide build artifact to other jobs in workflow
* [Download-Artifact](https://github.com/actions/download-artifact) - Download artifact provided by other jobs to workflow

### External

* [Version-Increment](https://github.com/reecetech/version-increment) - increment version based on tags
* [Push-Protected](https://github.com/casperwa/push-protected) - Push to protected branches
* [Release-Action](https://github.com/ncipollo/release-action)

### Verification (verify_repo_vars_and_secrets)

Here the presence of any kind of required repo variables and secrets is checked.
This is supposed to run at the beginning to make sure any changed to the repo only happen if the required data is available.
The required data like secrets can be grabed right from the repositories secrets from from input values, usually supplied by a claller workflow from the repository this workflow is supposed to run on.
The verified data is available to upcoming jobs.

### Query Latest Release (get_altest_release)

Next it is mendatory to test if a "latest" release already exist.
On the one hand to grab data from it like its publish date and the draft flag, on the other hand that this release it not the first one for this repository.
The queried data is provided for all upcoming jobs as well.

### Increment Version (increment-version)

This job uses runs the already mentioned [GitHub-Query](https://github.com/ynput/github-query) Action, which currently returns the a PR label list relevant for version bumping as well as a version increment suggestion.
These return values get validated to check if creation of another release even makes sense. Will returns an error notification in case not.
If the return values get valdiated successfully the [Version-Increment](https://github.com/reecetech/version-increment) Action runs using the increment value as input.
Finally it returns the next version tag suggestion.

### Merge to Main (merge-to-main)

Checkout the repositories develop branch and merges it into the protected main branch.
This runs the [Push-Protected](https://github.com/casperwa/push-protected) Action to push the changes to back to the remotes main branch right away.

### Build from Main
