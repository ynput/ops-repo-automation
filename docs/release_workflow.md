# Release Workflow

Meant to automate any tasks related to release creation.

## Intention

The Release Workflow is meant to have a one-click solution to handling all release related tasks.
This includes validation, merging branches, creating artifacts and so on.

## Requirements

Repository Secrets

* token - usually a bot token - Enables automated pushing and repository administration
* user - usually a bot username - Used for commit authentication
* email - usually a bot email - Used for commit authentication

Inputs

* draft - Create release as a draft or publish right away (Tag gets created when release is published - Drafts are not tagged)
* release_overwrite - Set the release tag right away - overwrites calculated one
* release_name - Set release name (usually same as tag)

Repository Variables

* PROJECT_NAME - used for package name when running *create_package.py*
* MAIN_BRANCH - name of the main branch (usually 'main')
* PATCH_BUMP_LABEL - comma separated list of PR-Labels to bump patch version (supports "," and ", " separation)
* MINOR_BUMP_LABEL - comma separated list of PR-Labels to bump minor version (supports "," and ", " separation)
* CHANGELOG_ORDER - if present custom changelog will be created based on this comma separated label order (supports "," and ", " separation)

## Main Features

### Automatic version increment

Uses a github [action](https://github.com/ynput/github-query) to calculate an expected version increment.
For this to work it requires repository variables to be set.

The repository calling the release-workflow should provide these repository variables

* **PATCH_BUMP_LABEL** - <mark>Required</mark> list of PR-Labels to bump patch version
* **MINOR_BUMP_LABEL** - <mark>Required</mark> list of PR-Labels to bump minor version
* **MAJOR_BUMP_LABEL** - <mark>Optional</mark> list of PR-Labels to bump major version (Will just be skipped if not set)

### Custom Changelog

Requires the repository variable `CHANGELOG_ORDER` to be set.
Based on this order of pull request labels a changelog containing pull request titles and their descriptions will be created and assigned to the release on github.
This is just looks for the label names so any typos might causes missing information in the generated changelog.

## Workflow Structure

The workflow is split into multiple jobs, each handlings a different kind of logic.
Additionally the jobs run certain dedicated Github Actions which are stand-alone units
Some examples in use right now (27.09.24)

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
The required data like secrets can be grabbed right from the repositories secrets from from input values, usually supplied by a caller workflow from the repository this workflow is supposed to run on.
The verified data is available to upcoming jobs.

### Query Latest Release (get_latest_release)

Next it is mandatory to test if a "latest" release already exist.
On the one hand to grab data from it like its publish date and the draft flag, on the other hand that this release it not the first one for this repository.
The queried data is provided for all upcoming jobs as well.

### Increment Version (increment-version)

This job uses runs the already mentioned [GitHub-Query](https://github.com/ynput/github-query) Action, which currently returns the a PR label list relevant for version bumping as well as a version increment suggestion.
These return values get validated to check if creation of another release even makes sense. Will returns an error notification in case not.
If the return values get validated successfully the [Version-Increment](https://github.com/reecetech/version-increment) Action runs using the increment value as input.
Finally it returns the next version tag suggestion.

### Merge to Main Branch (merge-to-main)

Checkout the repositories protected main branch and merges the develop branch into it.
This runs the [Push-Protected](https://github.com/casperwa/push-protected) Action to push the changes to back to the remotes main branch right away.

### Build from Main Branch (build-from-main)

Checkout the repositories protected main branch and build an artifact from it.
This means a bunch of steps need to happen in order:

1. Update the package.py files version variable
1. Run `python create_package.py --output <output-dir>`, updates additional version numbers as well
1. Run `git add . -- ':!<artifact-dir>/<artifact-file>'` while excluding the artifact file
1. Run [Push-Protected](https://github.com/casperwa/push-protected) Action to update remote main branch
1. Upload the build artifact to the workflow

### Create Release (create-release)

Now the artifact uploaded by `build-from-main` job gets downloaded.
Next a new release gets created using [Release-Action](https://github.com/ncipollo/release-action) by default as draft release.

### Update Develop Branch (update-develop)

This job runs in parallel with `create-release` since they don't depend on each other.

To bring the develop branch up to date with main again a couple of steps are necessary.

1. Check out develop branch and merge remote main branch into it
1. Update version variable in `package.py` to `next-version+dev`
1. Build artifact again by running `python create_package.py --output <artifact-dir>` to update all related version numbers
1. Push to the remote develop using [Push-Protected](https://github.com/casperwa/push-protected).

### Verify Release (verify-release)

This jobs starts by querying the latest release as draft or not depending on the initial draft option.
Then it checks if the found release has teh expected tag assigned to it.
If this should be not the case it errors with an error notification and informs the user that something didn't work out as expected.
