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

	def move_servers(self, srv_id, group_id):
		server = self.build_server_object()
		server.assign_group(srv_id, group_id)
		self.log(srv_id, group_id)

	def log(self, srv_id, group_id):
		with open('log/clean.log', 'a') as f:
			log_msg = "%s     Move server_id: %s to group: %s \n" % (datetime.datetime.utcnow(), srv_id, group_id)
			f.write(log_msg)
