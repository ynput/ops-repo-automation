# Assign PRs to Project automatically

## Caller Workflow

Intended to be triggered on PR creation automatically.
Checks first for the source repository the PR was created from.
In case the PR was created from a fork it will skip the automated project assignment workflow call.
This happens intentionally due to the fact that the Bot Token used for project related commands is exclusive to the organization (ynput) and not available to PRs created from forks.

Therefor these PRs from forks still need get assign to the project manually.

When the PRs source repository is identical to the repository the workflow is run from it will call the automated assignment workflow

## Called Workflow

in `pr_to_project.yml` the token gets checked first. Afterwards the gh command runs to assign the PR which triggered the workflow to a project.
