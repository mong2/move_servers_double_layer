import cloudpassage
import json
import datetime
import pytz
import dateutil.parser
from lib.server_controller import ServerController
from lib.group_controller import GroupController
import os
import yaml

PORTAL_CONFIG = os.path.join(os.path.dirname(__file__), 'configs/portal.yml')


class Clean(object):
    def __init__(self):
        self.configs = yaml.load(file(PORTAL_CONFIG, 'r'))
        self.server = ServerController(self.configs["key_id"], self.configs["secret_key"])
        self.group = GroupController(self.configs["key_id"], self.configs["secret_key"])
        self.time_gap = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=14))

    def move_new_servers(self):
        kwargs = {
                    "group_name": self.configs["newserver_group"],
                    "state": ['active', 'deactivated']
                }
        servers = self.server.filter_srv(self.server.index(**kwargs), server_label=None)
        groups = self.group.index()
        self.window_grp = self.group.find_group(groups, id=self.configs['windows_subgroup'])
        self.linux_grp = self.group.find_group(groups, id=self.configs['linux_subgroup'])

        for server in servers:
            srv_platform = server["platform"]
            srv_label = server["server_label"][:12]
            srv_kernel = server["kernel_name"]

            filtered_group = self.group.filtered_grp([self.window_grp["id"], self.linux_grp["id"]])
            designated_group = self.group.designated_grp(srv_kernel, srv_platform, filtered_group)

            if not designated_group:
                grp_name_window = "%s--%s" % (srv_kernel, srv_label)
                grp_name_linux = "%s--%s" % (srv_platform, srv_label)
                if srv_platform == 'windows':
                    parent_id = self.group.create_grp(srv_kernel, self.window_grp["id"])
                    child_id = self.group.create_grp(srv_label, parent_id)
                    self.server.move_servers(server, child_id, grp_name_window)
                else:
                    parent_id = self.group.create_grp(srv_platform, self.linux_grp["id"])
                    child_id = self.group.create_grp(srv_label, parent_id)
                    self.server.move_servers(server, child_id, grp_name_linux)
            else:
                grp_name = "%s--%s" % (designated_group["name"], srv_label)
                filtered_sub = self.group.filtered_grp([designated_group["id"]])
                if not self.group.find_group(filtered_sub, name=srv_label):
                    child_id = self.group.create_grp(srv_label, designated_group["id"])
                    self.server.move_servers(server, child_id, grp_name)
                else:
                    self.server.move_servers(server, self.group.find_group(filtered_sub, name=srv_label)["id"], grp_name)

    def move_deactivated_servers(self):
        retired_group = self.group.find_group(self.group.index(), id=self.configs["retired_group_id"])
        deactivated_servers = self.server.index(state=["deactivated"], last_state_change_lte=self.time_gap)
        filtered_servers = self.server.filter_srv(deactivated_servers, group_id=retired_group["id"])
        for srv in filtered_servers:
            self.server.move_servers(srv, retired_group["id"], retired_group["name"])


def main():
    clean = Clean()
    clean.move_new_servers()
    clean.move_deactivated_servers()

if __name__ == "__main__":
    main()
