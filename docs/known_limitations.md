# Workflow Limitations

## Types of limitations

I will split the limitations here in to categories:

* Github Workflow Limitations
* Ynput specific Limitations

## GitHub Workflow Limitations

### Type conversations

Github Action Workflows treat most data as strings even tho other data types like booleans or integer also exist, see [docs](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#literals).
Most logic will however check for string values that are either present or empty strings.
When using workflow_dispatch triggers any kind of text input gets converted to a string - due to the fact that a user can type any string.

Converting an input string to a number or boolean can be done using the from_json filter like described [here](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#operators)

### Reusable Workflows

In terms of reusable workflows you can nest them at a max of 4 levels.
See the docs [here](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#nesting-reusable-workflows).
So far this has not been an issue but the most complex workflow at the time of writing - release-trigger - got a max of 3 levels.
Additionally a caller workflow can call a max of 20 reusable workflows.

Additionally environment variables will not be passed on to called workflows.
Same goes for secrets - even tho secrets can be passed on explicitly using `secrets: inherit` as a parameter.
Referencing reusable workflows from private repositories won't work out of the box.
