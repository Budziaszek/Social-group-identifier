import random
from copy import deepcopy
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from UserAgent import UserAgent


class SiteModel(Model):
    tags = ["dog", "cat", "lama"]
    actions = ["write_comment", "write_post", "react", "share_post"]

    def __init__(self, num_agents):
        super().__init__()

        self.running = True
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.exp = np.random.exponential(1, num_agents)
        self.exp_normalized = [float(value) / max(self.exp) for value in self.exp]
        self.influence_values = deepcopy(self.exp_normalized)
        self.users = []

        # Create users
        for i in range(num_agents):
            user = UserAgent(i,
                             self.define_user_interests(),
                             self.define_user_actions_probabilities(),
                             self.define_user_influence(),
                             self)
            user.add_random_friends(round(random.choice(self.exp_normalized) * num_agents/3) + 1)
            self.schedule.add(user)
            self.users.append(user)

        self.datacollector = DataCollector(model_reporters={})

    def define_user_influence(self):
        return self.influence_values.pop()

    @staticmethod
    def define_user_interests():
        exp = list(np.random.normal(0, 1, len(SiteModel.tags)))
        values = [float(value) / 3 if abs(float(value) / 3) <= 1 else round(float(value) / 3) for value in exp]
        return {tag: values.pop() for tag in SiteModel.tags}

    def define_user_actions_probabilities(self):
        d = {}
        for action in SiteModel.actions:
            v = random.choice(self.exp_normalized) * 2
            if action is "react":
                v *= 1.5
            elif action is "share_post":
                v *= 0.7
            d[action] = v if abs(v) <= 1 else 1
        return d

    def step(self):
        print("\nNew cycle")
        self.datacollector.collect(self)
        self.schedule.step()
