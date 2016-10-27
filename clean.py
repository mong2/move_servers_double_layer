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

    def build_tree(self, server, designated_group, parent_grp, child_grp):
        if designated_group:
            filtered_sub = self.group.filtered_grp([designated_group["id"]])
            if not self.group.find_group(filtered_sub, name=child_grp):
                child_id = self.group.create_grp(child_grp, designated_group["id"])
                self.server.move_servers(server, child_id, child_grp)
            else:
                self.server.move_servers(server, self.group.find_group(filtered_sub, name=child_grp)["id"], child_grp)
        else:
            parent_id = self.group.create_grp(parent_grp, self.aws_grp["id"])
            child_id = self.group.create_grp(child_grp, parent_id)
            self.server.move_servers(server, child_id, child_grp)


    def move_new_servers(self):
        kwargs = {
                    "group_name": self.configs["newserver_group"],
                    "state": ['active', 'deactivated']
                }
        servers = self.server.index(**kwargs)
        groups = self.group.index()
        self.aws_grp = self.group.find_group(groups, id=self.configs['aws_group'])

        for server in servers:
            srv_platform = server["platform"]
            srv_plaform_version = "%s %s" % (srv_platform, server["platform_version"])
            srv_kernel = server["kernel_name"]

            filtered_group = self.group.filtered_grp([self.aws_grp["id"]])
            designated_group = self.group.designated_grp(srv_platform, filtered_group)

            if srv_platform == "windows":
                self.build_tree(server, designated_group, srv_platform, srv_kernel)
            else:
                self.build_tree(server, designated_group, srv_platform, srv_plaform_version)

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
