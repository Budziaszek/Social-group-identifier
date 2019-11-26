from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from UserAgent import UserAgent

class SiteModel(Model):
    def __init__(self, user_no):
        super().__init__()

        self.running = True
        self.num_agents = user_no
        self.schedule = RandomActivation(self)

        # Create users
        for i in range(user_no):
            user = UserAgent(user_no, self)

        self.datacollector = DataCollector(model_reporters={})

    def step(self):
        print("\nNew cycle")
        self.datacollector.collect(self)
        self.schedule.step()