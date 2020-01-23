import math
import random
from copy import deepcopy
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from RoleAgent import RoleAgent
from utils import define_user_interests, define_user_actions_probabilities
from UserAgent import UserAgent
from role_types import roles
from GroupAgent import GroupAgent

from data_collector_utils import get_number_of_post_written, biggest_group


class SiteModel(Model):

    def __init__(self, num_agents):
        super().__init__()

        self.running = True
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.schedule_groups = RandomActivation(self)
        self.schedule_roles = RandomActivation(self)
        self.exp = np.random.exponential(1, num_agents)
        self.exp_normalized = [float(value) / max(self.exp) for value in self.exp]
        self.influence_values = deepcopy(self.exp_normalized)
        self.users = []
        self.role_agents = []
        self.groups = []

        # Create users
        for i in range(num_agents):
            user = UserAgent(i,
                             define_user_interests(),
                             define_user_actions_probabilities(self.exp_normalized),
                             self.define_user_influence(),
                             self)
            self.schedule.add(user)
            self.users.append(user)
        for user in self.users:
            user.add_random_friends(round(math.ceil(random.choice(self.exp_normalized) * num_agents / 3)) + 1)
            user.expand_influence()

        self.datacollector = DataCollector(model_reporters={"biggestGroup": biggest_group},
                                           agent_reporters={"Post_written": get_number_of_post_written})

    def create_groups(self, num_groups):
        # Create groups
        for i in range(num_groups):
            group = GroupAgent(self.num_agents + i,  # groups ID are in range (num_agents, num_agents + num_groups)
                               self)
            self.schedule_groups.add(group)
            self.groups.append(group)

    def define_user_influence(self):
        return self.influence_values.pop()

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def step_groups(self):
        self.datacollector.collect(self)
        self.schedule_groups.step()

    def assign_roles_init(self, groups):
        # Create role agents
        for i, role in enumerate(roles):
            role_agent = RoleAgent(i, role, self)
            self.schedule_roles.add(role_agent)
            self.role_agents.append(role_agent)
        RoleAgent.groups = groups
        for agent in self.role_agents:
            agent.determine_users_roles()
