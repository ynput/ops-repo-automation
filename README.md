# Ayon-Automation
Collection of automation tools and github-workflows for Ayon related repositories.

# Release-Trigger-Workflow
Rolling release of a release trigger implementation customized for the Ayon workflows
## Expected Repository Variables and Secrets
See [here](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#creating-configuration-variables-for-a-repository) for details on how to create them.
* Secrets
  * YNPUT_BOT_TOKEN (str) - GitHub token used for the bot to run a workflow
  * CI_USER (str) - Username for the bot to authenticate for pushing (git config --global user.name)
  * CI_EMAIL (str) - E-Mail for the bot to authenticate for pushing (git config --global user.email)
* Variables
  * PROJECT_NAME (str) - name of the library, addon or whatever the repository contains
  * MAIN_BRANCH (str) - name of the main branch, usually "main"
  * PATCH_BUMP_LABEL ([str, str]) - bump the patch version if one of these labels (comma separated values) exist
  * MINOR_BUMP_LABEL ([str, str]) - bump the minor version if one of these labels (comma separated values) exist
