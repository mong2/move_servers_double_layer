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
            filtered_group = self.group.filtered_grp([self.configs['aws_group']])

            if not server["platform"]:
                pass
            elif server["platform"] == "windows":
                self.build_tree.build(server, filtered_group, server["platform"], server["kernel_name"])
            else:
                srv_plaform_version = "%s %s" % (server["platform"], server["platform_version"].split(".")[0])
                self.build_tree.build(server, filtered_group, server["platform"], srv_plaform_version)


def main():
    clean = Clean()
    clean.move_new_servers()

if __name__ == "__main__":
    main()
