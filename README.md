<b> Description </b>

Project to move all servers from a target server group into a subset of Linux and Windows server groups. The subset of server groups are separated by platforms then by their respective server labels.

The second functionality of this project moves all deactivated servers that are older than 14 days into a targeted retired group.

<b> Prerequisities: </b>

1. cloudpassage sdk (Can be installed here: https://github.com/cloudpassage/cloudpassage-halo-python-sdk/tree/develop)

2. Populate the following values in portal.yml (located in configs directory)

  * key_id, secret_key pair (This is your halo portal api_keys)

  * linux_subgroup (group_id for the target linux subgroup)

  * windows_subgroup (group_id for the target windows subgroup)

  * retired_group_id (group_id for the deactivated servers to be moved into)

  * newserver_group (name of the new server group)

  <i> Note: group_ids can be retrieved from the halo ui via v1/groups </i>


<b> Dependencies: </b>

1. Python 2.7.10
2. cloudpassage python package

<b> To use: </b>

```
python clean.py
```