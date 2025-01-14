# Development tasks

## Integration Testing

Right now the biggest missing part for this development setup is integration testing.
That means that e.g. release workflows can be tested fully automatically. The Repo reset workflow for the ayon-addon-action-testing repo was my starting point which I did not finish to extend to a full integration testing. It still requires manual work.
Ultimately any update to a workflow which is used called in the release workflow should trigger an automated run on a testing repo and report back if it worked or not.
This way a developer can know early on if something broke and what.

## Automated repo creation

The ayon-addon-template repository already provides a lot of great defaults. Only GitHub repository settings and branch setups wont be created for new repositories automatically.
Therefore a dedicated workflow would make a lot of sense.
The reset repo workflow can be used as a baseline here since it already incorporates most if not all of the requirements for new repos anyway.

Starting from job `reset-test-repo`, step `Create new Repo '${{ env.TARGET_REPO }}' from template '${{ env.TEMPLATE_REPO }}'` this already contains a blueprint for repository creation including at least most of the requirements for ynput repositories.
This includes especially all required secrets and variables needed by the release workflow.

## Enabling PR triggered workflows from Forks

Due to this being a security risk it is just disabled right now in `assign_pr_to_project.yml`
It might be an option to create a dedicated token that only got limited access to organization projects. The main issue here is that it would need write access to assign the PR which still shows an issue.

## Add tag-hash verification

We encountered the issue that the release workflow set the [tag to the wrong hash](https://github.com/ynput/ops-repo-automation/issues/29). This kinda behavior is critical to further processing of the packages.
So it would make sense to add a tag verification to the release workflow to make sure it fails when ever it didn't end up as expected.
This could be implemented to the 'build_from_branch'-workflow by saving the hash out from steps `Add changed files from ${{ vars.MAIN_BRANCH }}` and providing it as an output to verify in the end.
