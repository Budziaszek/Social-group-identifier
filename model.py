from random import random

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
        self.users = []

        # Create users
        for i in range(num_agents):
            user = UserAgent(i,
                             self.define_user_interests(),
                             self.define_user_actions_probabilities(),
                             self.define_user_influence(),
                             self)
            user.add_random_friends(random()*num_agents - 1)
            self.schedule.add(user)
            self.users.append(user)

        self.datacollector = DataCollector(model_reporters={})

    @staticmethod
    def define_user_influence():
        # TODO adjust the distribution of values (low number of influential users expected)
        return random()

    @staticmethod
    def define_user_interests():
        # TODO adjust the distribution of values
        return {tag: random() * 2 - 1 for tag in SiteModel.tags}

    @staticmethod
    def define_user_actions_probabilities():
        # TODO adjust the distribution of values
        return {action: random() for action in SiteModel.actions}

    def step(self):
        print("\nNew cycle")
        self.datacollector.collect(self)
        self.schedule.step()
