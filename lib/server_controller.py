import cloudpassage


class ServerController(object):

	def __init__(self, key_id, secret_key):
		self.key_id = key_id
		self.secret_key = secret_key

	def create_halo_session_object(self):
	    """create halo session object"""
	    session = cloudpassage.HaloSession(self.key_id, self.secret_key)
	    return session


	def build_server_object(self):
		"""create server object"""
		server_object = cloudpassage.Server(self.create_halo_session_object())
		return(server_object)

	def index(self, **kwargs):
		"""query all servers based on the filter"""
		s = self.build_server_object()
		return s.list_all(**kwargs)

	def filter_srv(self, servers, **kwargs):
		"""filter server output with specific requirement"""
		key, value = kwargs.items()[0]
		servers = [ x for x in servers if x[key] != value]
		return servers

	def move_servers(self, srv, group_id, group_name):
		"""Move server to another server group"""
		servers = self.build_server_object()
		servers.assign_group(srv["id"], group_id)
