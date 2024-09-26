# Intention

The Release Worflow is meant to have a one-click solution to handling all release related tasks.
This includes validation, merging branches, creating artifacts and so on.

## Structure

The workflow is split into multiple jobs, each handeling a different kind of logic.

### Verification (verify_repo_vars_and_secrets)

Here the presence of any kind of required repo variables and secrets is checked.
This is supposed to run at the beginning to make sure any changed to the repo only happen if the required data is available.
The required data like secrets can be grabed right from the repositories secrets from from input values, usually supplied by a claller workflow from the repository this workflow is supposed to run on.
The verified data is made available for all upcoming jobs.

### Query Latest Release (get_altest_release)

Next it is mendatory to test if a "latest" release already exist.
On the one hand to grab data from it like its publish date and the draft flag, on the other hand that this release it not the first one for this repository.
The queried data is provided for all upcoming jobs as well.

### Increment Version (increment-version)

This job uses the version tag queried by "get_altest_release" and increments its patch or minor level.
This is based on PR labels of merged Prs since the latest release.
Then the names of these labels get compared against a list of strings saved in the repo variable "PATCH_BUMP_LABEL" or "MINOR_BUMP_LABEL".
If there is a match for "PATCH_BUMP_LABEL" the patch version gets incremented (X.X.+1).
if there is a match for "MINOR_BUMP_LABEL" the minor version gets incremented (X.+1.X).
Here the minor version has higher priority.

### Merge to Main (merge-to-main)

Merges the develop branch into the protected main branch.

### Build from Main
