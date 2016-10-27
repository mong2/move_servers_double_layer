
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

    def designated_grp(self, srv_platform, filtered_group):
        return self.find_group(filtered_group, name=srv_platform)

    def build(self, server, filtered_group, parent_grp, child_grp):
        designated_group = self.designated_grp(parent_grp, filtered_group)

        if designated_group:
            filtered_sub = self.group.filtered_grp([designated_group["id"]])
            if not self.find_group(filtered_sub, name=child_grp):
                child_id = self.group.create_grp(child_grp, designated_group["id"])
                self.server.move_servers(server, child_id, child_grp)
            else:
                self.server.move_servers(server, self.find_group(filtered_sub, name=child_grp)["id"], child_grp)
        else:
            parent_id = self.group.create_grp(parent_grp, self.aws_grp)
            child_id = self.group.create_grp(child_grp, parent_id)
            self.server.move_servers(server, child_id, child_grp)