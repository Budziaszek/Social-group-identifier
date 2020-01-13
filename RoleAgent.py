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
            for user in group:
                self.check_criteria(user, group)

    @staticmethod
    def normalize(value, minimum, maximum, new_min=0, new_max=1):
        return ((value - min) / (maximum - minimum)) * (new_max - new_min) + new_min

    def check_influence_role(self, user, group):
        influence = RoleAgent.normalize(user.get_influence(group),
                                        min([u.get_influence(group) for u in group]),
                                        max([u.get_influence(group) for u in group]))
        activity = RoleAgent.normalize(user.get_activity(group),
                                       min([u.get_activity(group) for u in group]),
                                       max([u.get_activity(group) for u in group]))
        if self.role is "Spamer":
            if influence <= 0.3 and activity >= 0.7:
                user.add_role(self.role)
        elif self.role is "Celebryta":
            if influence >= 0.7 and activity <= 0.3:
                user.add_role(self.role)
        elif self.role is "Popularny":
            if influence >= 0.7 and activity >= 0.7:
                user.add_role(self.role)
        elif self.role is "Nowy":
            if influence <= 0.3 and activity <= 0.3:
                user.add_role(self.role)

    def check_neighbors_role(self, user, group):
        neighbors_in_group = user.get_number_of_neighbors_in_group(group)
        neighbors_outside_the_group = user.get_number_of_neighbors_outside_the_group(group)
        if self.role is "Koncentrator":
            if neighbors_in_group >= 0.7 and neighbors_outside_the_group < 0.7:
                user.add_role(self.role)
        elif self.role is "Pośrednik":
            if neighbors_in_group < 0.7 and neighbors_outside_the_group >= 0.7:
                user.add_role(self.role)
        elif self.role is "Wszędobylski":
            if neighbors_in_group >= 0.7 and neighbors_outside_the_group >= 0.7:
                user.add_role(self.role)

    def check_attitude_role(self, user):
        positive = user.get_number_of_positive_actions()
        negative = user.get_number_of_negative_actions()
        ratio = positive / negative
        if self.role is "Narzekacz":
            if ratio <= 0.3:
                user.add_role(self.role)
        elif self.role is "Komplemenciarz":
            if ratio >= 0.7:
                user.add_role(self.role)
        elif self.role is "Neutralny_Zbalansowany":
            if 0.3 < ratio < 0.7:
                user.add_role(self.role)

    def check_activities_role(self, user):
        comments = user.get_number_of_comments()
        posts = user.get_number_of_posts()
        shares = user.get_number_of_shares()
        reactions = user.get_number_of_reactions()
        total = comments + posts + shares + reactions
        if self.role is "Lurker":
            if (comments + posts) / total <= 0.3:
                user.add_role(self.role)
        elif self.role is "Komentujący":
            if comments / total >= 0.7:
                user.add_role(self.role)
        elif self.role is "Piszący":
            if posts / total >= 0.7:
                user.add_role(self.role)
        elif self.role is "Udostępniający":
            if shares / total >= 0.7:
                user.add_role(self.role)
        elif self.role is "Reagujący":
            if reactions / total >= 0.7:
                user.add_role(self.role)
        elif self.role is "Zbalansowany":
            if 0.15 < shares / total < 0.35 and 0.15 < comments / total < 0.35 and 0.15 < posts < 0.35 \
                    and 0.15 < reactions / total < 0.35:
                user.add_role(self.role)

    def check_criteria(self, user, group):
        if self.mode is self.WITH_NEGOTIATIONS:
            if self.role in roles_influence:
                self.check_influence_role(user, group)
            if self.role in roles_neighbors:
                self.check_neighbors_role(user, group)
            if self.role in roles_attitude:
                self.check_attitude_role(user)
            if self.role in roles_activities:
                self.check_activities_role(user)

    def negotiate(self):
        pass
