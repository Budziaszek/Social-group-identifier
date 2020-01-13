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


class SiteModel(Model):

    def __init__(self, num_agents):
        super().__init__()

        self.running = True
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.exp = np.random.exponential(1, num_agents)
        self.exp_normalized = [float(value) / max(self.exp) for value in self.exp]
        self.influence_values = deepcopy(self.exp_normalized)
        self.users = []
        self.role_agents = []

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

        self.datacollector = DataCollector(model_reporters={})

    def define_user_influence(self):
        return self.influence_values.pop()

    def step(self):
        print("\nNew cycle")
        self.datacollector.collect(self)
        self.schedule.step()

    def assign_roles_init(self, groups):
        # Create role agents
        for i, role in enumerate(roles):
            role_agent = RoleAgent(i, self, role)
            self.schedule.add(role_agent)
            self.role_agents.append(role_agent)
        RoleAgent.groups = groups
        for agent in self.role_agents:
            agent.determine_users_roles()
