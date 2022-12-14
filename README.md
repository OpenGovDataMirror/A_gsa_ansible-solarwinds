solarwinds [![circleci](https://circleci.com/gh/GSA/ansible-solarwinds.svg?style=svg)](https://circleci.com/gh/GSA/ansible-solarwinds)
=========

This ansible role installs and configures the solarwinds agent required to communicate with client machines for logging & monitoring.

Requirements
------------

Required Packages (this role requires access to the following packages/installers via an external repository)
- solarwinds.tar.gz - tar compressed redhat installer package
- solarwinds.msi - windows installer package

Role Variables
--------------

### Windows

| Variable | Default | Purpose |
| ------ | ------ | ------ |
| windows_solarwinds_agent_path | "C:\\Program Files (x86)\\SolarWinds\\Agent" | default windows install directory |
| windows_solarwinds_agent_url | "" | windows installer msi |
| windows_solarwinds_product_id | "" | windows product_id |
| windows_agent_log | "C:\Temp\Logs" | default agent windows log directory |

### Redhat

| Variable | Default | Purpose |
| ------ | ------ | ------ |
| redhat_solarwinds_agent_path | "/opt/solarwinds" | default redhat install directory |
| redhat_solarwinds_agent_url | "" | redhat installer rpm |

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
     - solarwinds
```

Public domain
-------------

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
