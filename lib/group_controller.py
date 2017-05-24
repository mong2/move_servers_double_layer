import cloudpassage


class GroupController(object):
    def __init__(self, key_id, secret_key):
        self.key_id = key_id
        self.secret_key = secret_key

    def create_halo_session_object(self):
        """create halo session object"""
        session = cloudpassage.HaloSession(self.key_id, self.secret_key)
        return session

    def build_server_group_object(self):
        """create halo server group object"""
        srv_grp_obj = cloudpassage.ServerGroup(self.create_halo_session_object())
        return(srv_grp_obj)

    def index(self):
        """query all server groups in halo"""
        groups = self.build_server_group_object()
        return groups.list_all()

    def show(self, group_id):
        """query detail information of a specific server group"""
        groups = self.build_server_group_object()
        return groups.describe(group_id)

    def filtered_grp(self, grp_name):
        """query all the subgroups of the specified server groups"""
        groups = self.index()
        sub_root = None
        for group in groups:
            if group["name"] == grp_name:
                sub_root = group
                groups.remove(group)
        return sub_root, groups

    def create_grp(self, grp_name, grp_id):
        """create new server group"""
        api = cloudpassage.HttpHelper(self.create_halo_session_object())
        data = {
            "group": {

                "name": grp_name,
                "parent_id": grp_id
            }
        }
        resp = api.post('/v1/groups', data)
        return resp["group"]["id"]
