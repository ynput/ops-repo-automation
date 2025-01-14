# Reusable Workflows

## Concept

Depending on the complexity of a github actions workflow these .yml files can become pretty long and difficult to read.
Therefore th e approach of reusable workflows exists.
It's similar to the concept of functions due to options to provide inputs and outputs as well es complexity encapsulation.

Additional this provides the benefit of reusability of logical parts in a workflow.
See [GitHub Docs](https://docs.github.com/en/actions/sharing-automations/reusing-workflows) for further details.

## Difference to Github Actions

At first glance reusable workflows seem to be a way easier solution then implementing a dedicated GitHub Action.
I like to differentiate the two options between logic that works completely on it's own and not context dependent - this would be a dedicated action like [Github-Query](https://github.com/ynput/github-query).

On the other hand reusable workflows are more logic that was made reusable after being part of a more complex system.
Therefore it's usually partly context dependent and can just be reused in other similar context like similar workflows.

## Benefits

* Increases readability due to a consistent scheme
* Shortens workflows
* Allows for easy adjustments through parameters
* Can be reused without the need to understand all the logic
