# Release Workflow

Meant to automate the process of release creation.

## Intention

The Release Workflow is meant to have a one-click solution to handling all release related tasks.
This includes validation, merging branches, creating artifacts and so on.

## Requirements

Inputs

* draft - Create release as a draft or publish right away
* release_overwrite - Set the release tag right away - overwrites calculated one

Repository Secrets

* token - usually a bot token - Enables automated pushing and repository administration
* user - usually a bot username - Used for commit authentication
* email - usually a bot email - Used for commit authentication

Repository Variables

* PROJECT_NAME - used for package name when running *create_package.py*
* MAIN_BRANCH - name of the main branch (usually 'main')
* PATCH_BUMP_LABEL - comma separated list of PR-Labels to bump patch version (supports "," and ", " separation)
* MINOR_BUMP_LABEL - comma separated list of PR-Labels to bump minor version (supports "," and ", " separation)
* CHANGELOG_ORDER - if present custom changelog will be created based on this comma separated label order (supports "," and ", " separation)

## Main Features

Uses a github [action](https://github.com/ynput/github-query) to provide some main features:

* Automatic version increment
* Custom Changelog

## How to re-run release workflow

First delete the already present release or release draft.
removing release drafts before hand isn't strictly necessary but we should try to keep it clean and still do it.
Additionally the tag needs to be deleted otherwise the re-run will be blocked.
This will cause additional merges from the develop branch to the main branch and back back won't effect the code and version in any way.

### Automatic version increment

Uses a github [action](https://github.com/ynput/github-query) to calculate an expected version increment.
The repository calling the release-workflow should - as already mentioned - provide these repository variables.

* PATCH_BUMP_LABEL - <mark>Required</mark>
* MINOR_BUMP_LABEL - <mark>Required</mark>
* MAJOR_BUMP_LABEL - <mark>Optional</mark>

### Custom Changelog

Requires the repository variable `CHANGELOG_ORDER` to be set.
Example: `feature,enhancement,bugfix`

Based on this order of pull-request labels a changelog containing pull-request titles and their descriptions will be created and assigned to the release on github.
This just looks for the label names. So any typos might causes missing information in the generated changelog.
It uses the pull-request titles for the changelog entries and adds any found changelog description as details.

## GitHub Actions in use

Here's an overview of the dedicated GitHub Actions currently used in the release workflow. (02.12.24)

### Ynput-Owned

* [GitHub-Query](https://github.com/ynput/github-query) - used for pull-request data collection

### Github-Owned

* [Checkout](https://github.com/actions/checkout) - checkout repository
* [Upload-Artifact](https://github.com/actions/upload-artifact) - Provide build artifact to other jobs in workflow
* [Download-Artifact](https://github.com/actions/download-artifact) - Download artifact provided by other jobs to workflow

### External

* [Version-Increment](https://github.com/reecetech/version-increment) - increment version based on tags
* [Push-Protected](https://github.com/casperwa/push-protected) - Push to protected branches
* [Release-Action](https://github.com/ncipollo/release-action)

## Workflow Structure

The workflow is split into multiple jobs, each handlings a different kind of logic.
These logic is run in on of three different ways depending on the job:

* Referencing a Github Actions
* Referencing a reusable workflow
* Running the logic right inside the job

Most of the jobs call a reusable workflow tpo provided more easy reusability.

### Verification

job-names:

* verify-latest-release
* verify-repo-secrets
* verify-repo-vars
* validate-pr-information

The verification jobs run right at the beginning and are responsible for checking of the existents of all required information, like repo-vars and secrets.
Additionally it validates that existing releases are present as well as running a query for present PR-information (using [GitHub-Query](https://github.com/ynput/github-query)) to make sure a new release can be created.
The verified data is available to upcoming jobs.
The queried data is provided for all upcoming jobs as well.

### Increment Version

job-name: increment-version

If the return values get validated successfully the [Version-Increment](https://github.com/reecetech/version-increment) Action runs using the increment value as input.
Finally it returns the next version tag suggestion.
It will also handle any kind of manual overwrites and pass these on instead.

### Merge to Main Branch

job-name: merge-to-main

Checkout the provided `checkout_branch` and merges the provided `merge_from_branch` into it.
Will also work for protected branches due to the [Push-Protected](https://github.com/casperwa/push-protected).

### Build from Main Branch

job-name: build-from-main

Checkout the provided `branch_name` and build an artifact from it.
This means the following logic gets executed:

1. Update the package.py files version variable
1. Run `python create_package.py --output <output-dir>`, updates additional version numbers as well
1. Run `git add . -- ':!<artifact-dir>/<artifact-file>'` while excluding the artifact file
1. Tag gets created if changes were detected
1. Run [Push-Protected](https://github.com/casperwa/push-protected) Action to update remote main branch
1. Upload the build artifact to the workflow

### Create Release

job-name: create-release

Now the artifact uploaded by `build-from-main` job gets downloaded.
Next a new release gets created using [Release-Action](https://github.com/ncipollo/release-action) by default as draft release.
The formerly created artifact gets attached to the created release.

### Update Develop Branch

job-name: update-develop

This job runs in parallel with `create-release` cause they don't depend on each other.
To bring the provided `checkout_branch` up to date with provided `update_from_branch` these steps are required.

1. Check out the `checkout_branch` branch and merge remote `update_from_branch` into it
1. Update version variable in `package.py` to `next-version+dev`
1. Build artifact again by running `python create_package.py --output <artifact-dir>` to update all related version numbers
1. Push to the remote develop using [Push-Protected](https://github.com/casperwa/push-protected).

### Verify Release

job-name: verify-release

Now the just created release gets queried as draft or not depending on the initial draft option.
Then it checks if the found release has the expected tag assigned to it.
If this should be not the case an error notification will occur and informs the user that something didn't work out as expected.
