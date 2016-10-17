import cloudpassage
import json

class GroupController(object):
	def __init__(self, key_id, secret_key):
		self.key_id = key_id
		self.secret_key = secret_key

	def create_halo_session_object(self):
	    """create halo session object"""
	    session = cloudpassage.HaloSession(self.key_id, self.secret_key)
	    return session

	def build_server_group_object(self):
		srv_grp_obj = cloudpassage.ServerGroup(self.create_halo_session_object())
		return(srv_grp_obj)

	def index(self):
		groups = self.build_server_group_object()
		return groups.list_all()

	def filtered_grp(self, group_ids = []):
		api = cloudpassage.HttpHelper(self.create_halo_session_object())
		filtered_group = []
		for group_id in group_ids:
			resp = api.get("/v1/groups?parent_id=%s" % group_id)
			filtered_group.extend(resp["groups"])
		return filtered_group

	def find_group(self, groups, **kwargs):
		key, value = kwargs.items()[0]
		if key == 'id':
			for group in groups:
				if group[key] == value:
					return group
		else:
			for group in groups:
				if group[key] == value:
					return group
		return None

	def create_grp(self, grp_name, grp_id):
		api = cloudpassage.HttpHelper(self.create_halo_session_object())
		data = {
			"group": {

				"name": grp_name,
				"parent_id": grp_id
			}
		}
		resp = api.post('/v1/groups', data)
		return resp["group"]["id"]

	def designated_grp(self, srv_kernel, srv_platform, filtered_group):
		if srv_platform == "windows":
			return self.find_group(filtered_group, name=srv_kernel)
		return self.find_group(filtered_group, name=srv_platform)

