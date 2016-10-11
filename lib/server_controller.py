import cloudpassage
from collections import defaultdict


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

	def index(self, group_name=None, state=[]):
		s = self.build_server_object()
		return s.list_all(group_name=group_name, state=state)

	def filter_srv_label(self, group_name=None, state=[]):
		servers = self.index(group_name=group_name, state=state)
		servers = [x for x in servers if x['server_label']]
		return servers

	def move_servers(self, srv_id, group_id):
		server = self.build_server_object()
		server.assign_group(srv_id, group_id)
