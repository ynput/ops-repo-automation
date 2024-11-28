# Workflow to push caller workflows

Update/push caller workflows to many repos at once.

## Intention

Caller-Workflows are the connection between the ynput repos and the automation workflows in ops-repo-automation.
Workflows will change over time due to changing requirements just as their corresponding caller workflows.
Therefore we need a way to update these caller workflows at scale. Just updating them manually isn't an option, way to many repos.
