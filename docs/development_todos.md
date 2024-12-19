# Development tasks

## Integration Testing

Right now the biggest missing part for this development setup is integration testing.
That means that e.g. release workflows can be tested fully automatically. The Repo reset workflow for the ayon-addon-action-testing repo was my starting point which I did not finish to extend to a full integration testing. It still requires manual work.
Ultimately any update to a workflow which is used called in the release workflow should trigger an automated run on a testing repo and report back if it worked or not.
This way a developer can know early on if something broke and what.

## Automated repo creation

The ayon-addon-template repository already provides a lot of great defaults. Only github repo settings and branch setups wont be created for new repositories automatically.
Therefore a dedicated workflow would make a lot of sense.
The reset repo workflow can be used as a baseline here since it already incorporates most if not all of the requirements for new repos anyway.
