import random
from copy import deepcopy
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from utils import define_user_interests, define_user_actions_probabilities
from UserAgent import UserAgent


class SiteModel(Model):

    def __init__(self, num_agents):
        super().__init__()

        self.running = True
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.exp = np.random.exponential(1, num_agents)
        self.exp_normalized = [float(value) / max(self.exp)
                               for value in self.exp]
        self.influence_values = deepcopy(self.exp_normalized)
        self.users = []

        # Create users
        for i in range(num_agents):
            user = UserAgent(i,
                             define_user_interests(),
                             define_user_actions_probabilities(
                                 self.exp_normalized),
                             self.define_user_influence(),
                             self)
            user.add_random_friends(
                round(random.choice(self.exp_normalized) * num_agents / 3) + 1)
            self.schedule.add(user)
            self.users.append(user)

        self.datacollector = DataCollector(model_reporters={})

    def define_user_influence(self):
        return self.influence_values.pop()

    def step(self):
        print("\nNew cycle")
        self.datacollector.collect(self)
        self.schedule.step()
