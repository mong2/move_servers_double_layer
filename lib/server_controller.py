import cloudpassage
import datetime


class ServerController(object):

	def __init__(self, key_id, secret_key):
		self.key_id = key_id
		self.secret_key = secret_key

	def create_halo_session_object(self):
	    """create halo session object"""
	    session = cloudpassage.HaloSession(self.key_id, self.secret_key)
	    return session


	def build_server_object(self):
		server_object = cloudpassage.Server(self.create_halo_session_object())
		return(server_object)

	def index(self, **kwargs):
		s = self.build_server_object()
		return s.list_all(**kwargs)

	def filter_srv(self, servers, **kwargs):
		key, value = kwargs.items()[0]
		servers = [ x for x in servers if x[key] != value]
		return servers

	def move_servers(self, srv, group_id, group_name):
		servers = self.build_server_object()
		servers.assign_group(srv["id"], group_id)
		self.log(srv, group_id, group_name)

	def log(self, server, group_id, group_name):
		with open('log/clean.log', 'a') as f:
			log_msg = "%s     Moved server label: %s (server_id: %s) from group name: %s (group_id: %s) to group name: %s (group_id: %s) \n" % (datetime.datetime.utcnow(),
																																				server["server_label"],
																																				server["id"],
																																				server["group_name"],
																																				server["group_id"],
																																				group_name, group_id)
			f.write(log_msg)
