# How to troubleshoot workflow issues

The troubleshooting approaches will go from the easiest and easy to stop things to more difficult cases from top to bottom.

## Notifications

If an issue or potential issue was expected and handled appropriately, you will see a notification at the bottom of the summary page.
Just clicking on it will show you the exact workflow step which triggered the notification and which logic caused it.

Any detected issues or potential issues will be marked as warnings or errors. The basic notifications without are nothing to worry about.

## Data related issues

Any data related issues like missing data, wrongly assigned data or issues in the changelog outputs are most likely related to behavior in the [GitHub-Query Action](https://github.com/ynput/github-query)

## Logic related issues

In these cases you will need to dive into the workflow code itself and start debugging - usually you can check the data which was present at the time an error occurred at least for the environment variables in every step.
