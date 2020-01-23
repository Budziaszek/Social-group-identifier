from mesa import Agent

from role_types import roles_influence, roles_neighbors, roles_activities, roles_attitude


class RoleAgent(Agent):
    groups = []
    WITH_NEGOTIATIONS = "negotiations"
    WITHOUT_NEGOTIATIONS = "no_negotiations"
    mode = WITHOUT_NEGOTIATIONS

    def __init__(self, unique_id, role, model):
        super().__init__(unique_id, model)
        self.role = role
        self.users_assigned = []

    def determine_users_roles(self):
        for group in self.groups:
            for user in group.group_members:
                self.check_criteria(user, group)

    @staticmethod
    def normalize(value, minimum, maximum, new_min=0, new_max=1):
        if maximum == 0:
            return value
        return ((value - minimum) / (maximum - minimum)) * (new_max - new_min) + new_min

    def check_influence_role(self, user, group):
        influence = RoleAgent.normalize(user.get_influence_by_edges(group),
                                        min([u.get_influence_by_edges(group) for u in group.group_members]),
                                        max([u.get_influence_by_edges(group) for u in group.group_members]))
        activity = RoleAgent.normalize(user.get_activity_by_edges(group),
                                       min([u.get_activity_by_edges(group) for u in group.group_members]),
                                       max([u.get_activity_by_edges(group) for u in group.group_members]))
        if self.role == "Spamer":
            if influence <= 0.3 and activity >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Celebryta":
            if influence >= 0.7 and activity <= 0.3:
                user.add_role(self.role, group)
        elif self.role == "Popularny":
            if influence >= 0.7 and activity >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Nowy":
            if influence <= 0.3 and activity <= 0.3:
                user.add_role(self.role, group)

    def check_neighbors_role(self, user, group):
        neighbors_in = RoleAgent.normalize(user.get_number_of_neighbors_in_group(group),
                                           min([u.get_number_of_neighbors_in_group(group) for u in
                                                group.group_members]),
                                           max([u.get_number_of_neighbors_in_group(group) for u in
                                                group.group_members]))
        neighbors_outside = RoleAgent.normalize(user.get_number_of_neighbors_outside_the_group(group),
                                                min([u.get_number_of_neighbors_outside_the_group(group) for u in
                                                     group.group_members]),
                                                max([u.get_number_of_neighbors_outside_the_group(group) for u in
                                                     group.group_members]))
        if self.role == "Koncentrator":
            if neighbors_in >= 0.7 and neighbors_outside < 0.7:
                user.add_role(self.role, group)
        elif self.role == "Pośrednik":
            if neighbors_in < 0.7 and neighbors_outside >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Wszędobylski":
            if neighbors_in >= 0.7 and neighbors_outside >= 0.7:
                user.add_role(self.role, group)

    def check_attitude_role(self, user, group):
        positive = RoleAgent.normalize(user.get_number_of_positive_actions(group),
                                       min([u.get_number_of_positive_actions(group) for u in group.group_members]),
                                       max([u.get_number_of_positive_actions(group) for u in group.group_members]))
        negative = RoleAgent.normalize(user.get_number_of_negative_actions(group),
                                       min([u.get_number_of_negative_actions(group) for u in group.group_members]),
                                       max([u.get_number_of_negative_actions(group) for u in group.group_members]))
        ratio = positive / negative if negative > 0 else int(positive > 0)
        if self.role == "Narzekacz":
            if ratio <= 0.3:
                user.add_role(self.role, group)
        elif self.role == "Komplemenciarz":
            if ratio >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Neutralny_Zbalansowany":
            if 0.3 < ratio < 0.7:
                user.add_role(self.role, group)

    def check_activities_role(self, user, group):
        comments = user.get_number_of_comments()
        posts = user.get_number_of_posts()
        shares = user.get_number_of_shares()
        reactions = user.get_number_of_reactions()
        total = comments + posts + shares + reactions
        if self.role == "Lurker":
            if (comments + posts) / total <= 0.3:
                user.add_role(self.role, group)
        elif self.role == "Komentujący":
            if comments / total >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Piszący":
            if posts / total >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Udostępniający":
            if shares / total >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Reagujący":
            if reactions / total >= 0.7:
                user.add_role(self.role, group)
        elif self.role == "Zbalansowany":
            if 0.15 < shares / total < 0.35 and 0.15 < comments / total < 0.35 and 0.15 < posts < 0.35 \
                    and 0.15 < reactions / total < 0.35:
                user.add_role(self.role, group)

    def check_criteria(self, user, group):
        if self.mode is self.WITHOUT_NEGOTIATIONS:
            if self.role in roles_influence:
                self.check_influence_role(user, group)
            if self.role in roles_neighbors:
                self.check_neighbors_role(user, group)
            if self.role in roles_attitude:
                self.check_attitude_role(user, group)
            if self.role in roles_activities:
                self.check_activities_role(user, group)

    def negotiate(self):
        pass
