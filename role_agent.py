from itertools import combinations
from math import floor

from mesa import Agent

from config import CURR_MODE, MODE_WITHOUT_NEGOTIATIONS, MODE_WITH_NEGOTIATIONS
from role_types import roles_influence, roles_neighbors, roles_activities, roles_attitude, get_name


class RoleAgent(Agent):
    group = None
    arr_inf = None
    arr_act = None
    arr_pos = None
    arr_neg = None
    arr_n_in = None
    arr_n_out = None

    def __init__(self, unique_id, role, model):
        super().__init__(unique_id, model)
        self.role = role
        self.selected = []
        self.dictionary = {}

    @staticmethod
    def calculate_parameters(group):
        RoleAgent.group = group

        RoleAgent.arr_inf = [u.influence_by_edges for u in RoleAgent.group.group_members]
        RoleAgent.arr_act = [u.activity_by_edges for u in RoleAgent.group.group_members]

        RoleAgent.arr_pos = [u.number_of_positive_actions for u in RoleAgent.group.group_members]
        RoleAgent.arr_neg = [u.number_of_negative_actions for u in RoleAgent.group.group_members]

        RoleAgent.arr_n_in = [u.number_of_neighbors_in_group for u in RoleAgent.group.group_members]
        RoleAgent.arr_n_out = [u.number_of_neighbors_outside_the_group for u in RoleAgent.group.group_members]

    def determine_users_roles(self):
        self.selected = {}
        self.dictionary = {}

        for user in RoleAgent.group.group_members:
            if CURR_MODE is MODE_WITHOUT_NEGOTIATIONS:
                self.check_criteria(user)
            else:
                self.check_criteria(user, self.dictionary)
        if self.role in roles_influence:
            num_of_users = floor(len(RoleAgent.group.group_members) / (len(roles_influence)))
        elif self.role in roles_neighbors:
            num_of_users = floor(len(RoleAgent.group.group_members) / (len(roles_neighbors)))
        elif self.role in roles_activities:
            num_of_users = floor(len(RoleAgent.group.group_members) / (len(roles_activities)))
        else:
            num_of_users = floor(len(RoleAgent.group.group_members) / (len(roles_attitude)))
        if num_of_users == 0:
            return
        self.selected = sorted(self.dictionary, key=self.dictionary.get)[0:num_of_users]

    @staticmethod
    def normalize(value, minimum, maximum, new_min=0, new_max=1):
        if maximum == 0:
            return 0
        elif maximum == minimum:
            return 1
        return ((value - minimum) / (maximum - minimum)) * (new_max - new_min) + new_min

    def assign_role(self, user, group):
        user.add_role(self.role, group)

    def check_influence_role(self, user, dictionary=None):
        influence = RoleAgent.normalize(user.get_influence_by_edges(RoleAgent.group),
                                        min(RoleAgent.arr_inf), max(RoleAgent.arr_inf))
        activity = RoleAgent.normalize(user.get_activity_by_edges(RoleAgent.group),
                                       min(RoleAgent.arr_act), max(RoleAgent.arr_act))

        if self.role == "Spamer":
            if dictionary is None and influence <= 0.3 and activity >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - influence) + abs(1.0 - activity)
        elif self.role == "Celebryta":
            if dictionary is None and influence >= 0.7 and activity <= 0.3:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - influence) + abs(0.0 - activity)
        elif self.role == "Popularny":
            if dictionary is None and influence >= 0.7 and activity >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - influence) + abs(1.0 - activity)
        elif self.role == "Nowy":
            if dictionary is None and influence <= 0.3 and activity <= 0.3:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - influence) + abs(0.0 - activity)

    def check_neighbors_role(self, user, dictionary=None):
        neighbors_in = RoleAgent.normalize(user.get_number_of_neighbors_in_group(RoleAgent.group),
                                           min(RoleAgent.arr_n_in), max(RoleAgent.arr_n_in))
        neighbors_outside = RoleAgent.normalize(user.get_number_of_neighbors_outside_the_group(RoleAgent.group),
                                                min(RoleAgent.arr_n_out), max(RoleAgent.arr_n_out))
        if self.role == "Koncentrator":
            if dictionary is None and neighbors_in >= 0.7 and neighbors_outside < 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - neighbors_in) + abs(0.0 - neighbors_outside)
        elif self.role == "Pośrednik":
            if dictionary is None and neighbors_in < 0.7 and neighbors_outside >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - neighbors_in) + abs(1.0 - neighbors_outside)
        elif self.role == "Wszędobylski":
            if dictionary is None and neighbors_in >= 0.7 and neighbors_outside >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - neighbors_in) + abs(1.0 - neighbors_outside)

    def check_attitude_role(self, user, dictionary=None):
        positive = RoleAgent.normalize(user.get_number_of_positive_actions(RoleAgent.group),
                                       min(RoleAgent.arr_pos), max(RoleAgent.arr_pos))
        negative = RoleAgent.normalize(user.get_number_of_negative_actions(RoleAgent.group),
                                       min(RoleAgent.arr_neg), max(RoleAgent.arr_neg))
        ratio = positive / negative if negative > 0 else int(positive > 0)

        if self.role == "Narzekacz":
            if dictionary is None and ratio <= 0.3:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - ratio)
        elif self.role == "Komplemenciarz":
            if dictionary is None and ratio >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - ratio)
        elif self.role == "Neutralny_Zbalansowany":
            if dictionary is None and 0.3 < ratio < 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.5 - ratio)

    def check_activities_role(self, user, dictionary=None):
        comments = user.get_number_of_comments()
        posts = user.get_number_of_posts()
        shares = user.get_number_of_shares()
        reactions = user.get_number_of_reactions()
        total = comments + posts + shares + reactions

        if total == 0:
            return

        v1 = comments / total
        v2 = posts / total
        v3 = shares / total
        v4 = reactions / total

        if total == 0:
            return
        if self.role == "Lurker":
            if dictionary is None and v4 >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - v1) + abs(0.0 - v2) + abs(0.0 - v3) + abs(1.0 - v4)
        elif self.role == "Komentujący":
            if dictionary is None and v1 >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(1.0 - v1) + abs(0.0 - v2) + abs(0.0 - v3) + abs(0.0 - v4)
        elif self.role == "Piszący":
            if dictionary is None and v2 >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - v1) + abs(1.0 - v2) + abs(0.0 - v3) + abs(0.0 - v4)
        elif self.role == "Udostępniający":
            if dictionary is None and v3 >= 0.7:
                self.assign_role(user, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.0 - v1) + abs(0.0 - v2) + abs(1.0 - v3) + abs(0.0 - v4)
        elif self.role == "Zbalansowany":
            if dictionary is None and 0.15 < v1 < 0.35 and 0.15 < v2 < 0.35 and 0.15 < v3 < 0.35 and 0.15 < v4 < 0.35:
                user.add_role(self.role, RoleAgent.group)
            elif dictionary is not None:
                dictionary[user] = abs(0.25 - v1) + abs(0.25 - v2) + abs(0.25 - v3) + abs(0.25 - v4)

    def check_criteria(self, user, dictionary=None):
        if self.role in roles_influence:
            self.check_influence_role(user, dictionary)
        if self.role in roles_neighbors:
            self.check_neighbors_role(user, dictionary)
        if self.role in roles_attitude:
            self.check_attitude_role(user, dictionary)
        if self.role in roles_activities:
            self.check_activities_role(user, dictionary)

    @staticmethod
    def negotiate(role_agents, users):
        if CURR_MODE is MODE_WITH_NEGOTIATIONS:
            role_groups = [roles_influence, roles_neighbors, roles_activities, roles_attitude]
            negotiations = {get_name(role): {} for role in role_groups}

            for user in users:
                for role_group in role_groups:
                    possible_roles = RoleAgent.check_best_role(user, role_group, role_agents)
                    for combination in combinations(possible_roles, 2):
                        if combination not in negotiations[get_name(role_group)]:
                            negotiations[get_name(role_group)][combination] = 1
                        negotiations[get_name(role_group)][combination] += 1
            return negotiations

    @staticmethod
    def check_best_role(user, roles, role_agents):
        user_role = None
        min_value = -1000
        possible_roles = []
        for role in roles:
            for role_agent in role_agents:
                if role_agent.role == role:
                    if user in role_agent.selected:
                        possible_roles.append(role)
                        if min_value > role_agent.dictionary[user] or user_role is None:
                            user_role = role
                            min_value = role_agent.dictionary[user]
        if user_role is not None:
            user.add_role(user_role, RoleAgent.group)
        return possible_roles
