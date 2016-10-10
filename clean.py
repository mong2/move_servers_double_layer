
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
		self.server = ServerController()
		self.group = GroupController()
		self.configs = yaml.load(file(PORTAL_CONFIG, 'r'))

	def move_new_servers(self):
		servers = self.server.filter_srv_label(group_name=self.configs["newserver_group"], state=["deactivated", "active"])
		groups = self.group.index()
		self.window_grp = self.group.find_group(groups, id=self.configs['windows_subgroup'])
		self.linux_grp = self.group.find_group(groups, id=self.configs['linux_subgroup'])

		for server in servers:
			srv_platform = server["platform"]
			srv_label = server["server_label"]
			srv_kernel = server["kernel_name"]
			filtered_group = self.group.filtered_grp([self.window_grp, self.linux_grp])
			desginated_grp = self.group.find_group(filtered_group, name=srv_platform)


			if not desginated_grp:
				if srv_platform == 'windows':
					parent_id = self.group.create_grp(srv_kernel, self.window_grp)
					child_id = self.group.create_grp(srv_label, parent_id)
					self.server.move_servers(server['id'], child_id)
				else:
					parent_id = self.group.create_grp(srv_platform, self.linux_grp)
					child_id = self.group.create_grp(srv_label, parent_id)
					self.server.move_servers(server['id'], child_id)
			else:
				filtered_sub = self.group.filtered_grp([desginated_grp])
				if not self.group.find_group(filtered_sub, name=srv_label):
					child_id = self.group.create_grp(srv_label, desginated_grp)
					self.server.move_servers(server['id'], child_id)
				else:
					self.server.move_servers(server['id'], self.group.find_group(filtered_sub, name=srv_label))

	def move_deactivated_servers(self):
		deactivated_servers = self.server.index(state=["deactivated"])
		for server in deactivated_servers:
			srv_last_seen = dateutil.parser.parse(server["last_state_change"])
			time_gap = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=14))
			if srv_last_seen < time_gap:
				print "Move server_id: %s to retired group" % (server["id"])
				self.server.move_servers(server["id"], self.configs["retired_group_id"])

def main():
	clean = Clean()
	clean.move_new_servers()
	clean.move_deactivated_servers()

if __name__ == "__main__":
    main()
