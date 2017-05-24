# move_servers_double_layer
<b> Description </b>

Project to move all servers from a target server group into a subset of Linux and Windows server groups. The subset of server groups are separated by platforms and platform versions.

<b> Prerequisities: </b>

1.	Populate the following values in portal.yml (located in configs directory)

  * newserver_group (name of the new server group)

  * log_destination (provide the absolute path where you would like your log file to be stored. i.e. C:\Cloudpassage      Halo\Logs\clean.log)

  * Specify api key pair and its related server group name under key_pairs, below is an example of server groups - AWS & Azure. Note: Server group name is case sensitive.

  ```
  key_pairs:
    AWS:
      key_id:
      secret_key:
    Azure:
      key_id:
      secret_key:
  ```

2.	Python 2.7.10

3.	cloudpassage python package (install via pip install cloudpassage)

4.	pytz (install via pip install pytz)]

5.	dateutil.parser (install via pip install python-dateutil)

<b> To use: </b>

```
python clean.py
```
