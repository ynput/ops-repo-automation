# Validate PR labels automatically

## Caller Workflow

Runs automatically on PR interaction like opening, editing, labeling or unlabeling.
Calls the main workflow and lets it check for "type: "-prefix in labels by default.

## Called Workflow

In `validate_pr_labels.yml` the token gets checked first. Afterwards the gh command runs to Query all assigned labels for the PR.
Then it acts depending on the absence or presence of a "type:"-prefix label with either an error or just a note that all was found as expected
