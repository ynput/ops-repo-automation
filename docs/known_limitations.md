# Workflow Limitations

## Type conversions

Github Action Workflows treat most data as strings even tho other data types like booleans or integer(number) also exist, see [docs](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#literals).
Most logic will however check for string values that are either present or empty strings.
When using workflow_dispatch triggers any kind of text input gets converted to a string - due to the fact that a user can type any string.

Converting an input string to a number or boolean can be done using the from_json filter like described [here](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#operators)

## Multiline Output

As a matter of fact Github Action Workflows are not able to assign multiline outputs to their GitHub specific variables.
There's however the option to reformat the multiline output into a single line string and extending it afterwards again using [delimiters](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#multiline-strings)

Here just an example from the [Github-Query](https://github.com/ynput/github-query) actions `action.yml` file using a randomized delimiter.

```bash
delimiter="$(openssl rand -hex 8)"
{
    echo "changelog<<${delimiter}"
    echo "$changelog"
    echo "${delimiter}"
} >> $GITHUB_OUTPUT
```

## Reusable Workflows

In terms of reusable workflows you can nest them at a max of 4 levels.
See the docs [here](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#nesting-reusable-workflows).
So far this has not been an issue but the most complex workflow at the time of writing - release-trigger - got a max of 3 levels.
Additionally a caller workflow can call a max of 20 reusable workflows.

Additionally environment variables will not be passed on to called workflows.
Same goes for secrets - even tho secrets can be passed on explicitly using `secrets: inherit` as a parameter.
Referencing reusable workflows from private repositories won't work out of the box.

## Organization secrets

When it comes to GitHub Action Workflows which are triggered automatically on PR creation or PR interaction the PRs source makes a difference.

At the time of writing (16.12.24) we encountered at least one issue in regards to organization secrets and PRs from forks.
Whenever a PR for on of the Ynput repositories gets created on of the action running immediately is `assign_pr_to_project.yml`.
This should assign the PR to the Ynteam Active project.

This works for any cases where the PR was created right from a branch within the Ynput repository.
The logic breaks tho when creating a PR from a fork of an ynput repository.
This happens due to the default behavior that organization secrets - which are required to interact with GitHub projects - are made available to a PR.
This wont happen by default for forked PRs and just pass on an empty string instead of the actual token fro security reasons.

Right now forked PRs simply get excluded from the automated project assignment. One way to solve that would be a dedicated token for just that purpose but that might also open up security risks.
