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
        self.keys = self.configs["key_pairs"]
        self.time_gap = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=14))

    def create_sesssion(self, key_pair):
        self.server = ServerController(key_pair["key_id"], key_pair["secret_key"])
        self.group = GroupController(key_pair["key_id"], key_pair["secret_key"])
        self.build_tree = BuildTreeController(self.server, self.group, self.configs)

    def move_new_servers(self):
        kwargs = {
            "group_name": self.configs["newserver_group"],
            "state": ['active', 'deactivated']
        }
        for grp_name, v in self.keys.iteritems():
            print grp_name, v

            self.create_sesssion(v)
            servers = self.server.index(**kwargs)
            sub_root, filtered_group = self.group.filtered_grp(grp_name)
            for server in servers:
                if not server["platform"]:
                    pass
                elif server["platform"] == "windows":
                    self.build_tree.build(server, sub_root, filtered_group, server["platform"], server["kernel_name"])
                else:
                    srv_plaform_version = "%s %s" % (server["platform"], server["platform_version"].split(".")[0])
                    self.build_tree.build(server, sub_root, filtered_group, server["platform"], srv_plaform_version)


def main():
    clean = Clean()
    clean.move_new_servers()

if __name__ == "__main__":
    main()
