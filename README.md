# move_servers_double_layer
<b> Description </b>

Project to move all servers from a target server group into a subset of Linux and Windows server groups. The subset of server groups are separated by platforms and platform versions.

<b> Prerequisities: </b>

1.	Populate the following values in portal.yml (located in configs directory)

  * key_id, secret_key pair (This is your halo portal api_keys)
    
  * aws_group (group_id for the target AWS subgroup)
    
  * newserver_group (name of the new server group)
    
  * log_destination (provide the absolute path where you would like your log file to be stored. i.e. C:\Cloudpassage      Halo\Logs\clean.log)

  <i> Note: group_ids can be retrieved from the halo ui via v1/group. </i>

2.	Python 2.7.10

3.	cloudpassage python package (install via pip install cloudpassage)

4.	pytz (install via pip install pytz)]

5.	dateutil.parser (install via pip install python-dateutil)

<b> To use: </b>

```
python clean.py
```
