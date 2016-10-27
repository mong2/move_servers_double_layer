import datetime
import pytz
import dateutil.parser
from lib.server_controller import ServerController
from lib.group_controller import GroupController
from lib.buildtree_controller import BuildTreeController
import os
import yaml

PORTAL_CONFIG = os.path.join(os.path.dirname(__file__), 'configs/portal.yml')


class Clean(object):
    def __init__(self):
        self.configs = yaml.load(file(PORTAL_CONFIG, 'r'))
        self.server = ServerController(self.configs["key_id"], self.configs["secret_key"])
        self.group = GroupController(self.configs["key_id"], self.configs["secret_key"])
        self.build_tree = BuildTreeController(self.server, self.group, self.configs)
        self.time_gap = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=14))

    def move_new_servers(self):
        kwargs = {
                    "group_name": self.configs["newserver_group"],
                    "state": ['active', 'deactivated']
                }
        servers = self.server.index(**kwargs)

        for server in servers:
            srv_plaform_version = "%s %s" % (server["platform"], server["platform_version"])
            filtered_group = self.group.filtered_grp([self.configs['aws_group']])

            if server["platform"] == "windows":
                self.build_tree.build(server, filtered_group, server["platform"], server["kernel_name"])
            else:
                self.build_tree.build(server, filtered_group, server["platform"], srv_plaform_version)

    def move_deactivated_servers(self):
        retired_group = self.group.show(self.configs["retired_group_id"])
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
