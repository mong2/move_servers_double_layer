
class BuildTreeController(object):
    def __init__(self, server_controller, group_controller, configs):
        self.server = server_controller
        self.group = group_controller
        self.aws_grp = configs["aws_group"]

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

    def create_family(self, parent_grp, child_grp):
        parent_id = self.group.create_grp(parent_grp, self.aws_grp)
        child_id = self.group.create_grp(child_grp, parent_id)
        return parent_id, child_id

    def check_child_grp_exist(self, child_grp, designated_group):
        child_exist = self.find_group(self.group.filtered_grp([designated_group["id"]]), name=child_grp)
        if not child_exist:
            return self.group.create_grp(child_grp, designated_group["id"])
        return child_exist["id"]

    def build(self, server, filtered_group, parent_grp, child_grp):
        designated_group = self.find_group(filtered_group, name=parent_grp)
        if designated_group:
            child_id = self.check_child_grp_exist(child_grp, designated_group)
            self.server.move_servers(server, child_id, child_grp)
        else:
            parent_id, child_id = self.create_family(parent_grp, child_grp)
            self.server.move_servers(server, child_id, child_grp)