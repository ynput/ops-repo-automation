# Security by Configuration

Implementing appropriate controls and settings to govern what can run and
when

* Workflow settings
  * Define workflow settings at Settings -> Actions -> General
  * Restrict Action permissions: Last option allows org owned, github owned and explicitly allowed actions (would reccomend)
  * Allow external collaborators to run workflows on PRs?
  * Default workflow permissions: Only read
* CODEWONERS file
  * Add CODEOWNERS file: Define groups or individuals reponsible for code files (Can automatically assign reviewers for PRs)
  * Check github documentation for details about [CODEOWNERS file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
* Protected Tags
  * Protect release tags to prevent them from being moved
  * Only spcific users should have permissions to modify and create tags
  * Allows consistency for CI/CD pipelines if tags are a trigger or a reference
* Protected Branches
  * PR before merging
  * Require status checks before merging
  * Require merge queue
  * Require deployments to succeed before merging
  * Settings -> Code and automation -> Branches -> Add branch protection rule
  * See [docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
* Repo Rules
  * 
