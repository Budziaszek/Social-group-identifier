from mesa import Agent
from random import sample, choice

from config import NUMBER_OF_INIT_TRIES, MIN_GROUP_CONSISTENCY, USERS_SEARCHED_PER_ITERATION, MAX_GROUP_MEMBERS


class GroupAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.group_members = []
        self._consistency = 0

    @property
    def size(self):
        return len(self.group_members)

    @property
    def is_empty(self):
        if not self.group_members:
            return True
        return False

    @staticmethod
    def calculate_consistency(users_to_check):
        value = 0
        for userA in users_to_check:
            for userB in users_to_check:
                value += userA.get_relation(userB)
        return value / (len(users_to_check) * (len(users_to_check) - 1))  # TODO check correctness of returned values

    def update_group(self):
        self._consistency = self.calculate_consistency(self.group_members)

        while self._consistency < MIN_GROUP_CONSISTENCY:
            self.delete_member()

            if len(self.group_members) < 3:  # Group has become too small and is exterminated
                self.group_members = []
                self._consistency = 0
                return False

            self._consistency = self.calculate_consistency(self.group_members)
        return True

    def delete_member(self):
        for i in range(len(self.group_members)):
            if self.calculate_consistency(self.group_members[:i] + self.group_members[i + 1:]) > self._consistency:
                del self.group_members[i]

    def search_new_members(self):
        for _ in range(USERS_SEARCHED_PER_ITERATION):
            if len(self.group_members) >= MAX_GROUP_MEMBERS:  # group is full, so leave loop and function
                break

            chosen_user = choice(self.model.users)
            while chosen_user in self.group_members:
                chosen_user = choice(self.model.users)

            if self.calculate_consistency([chosen_user] + self.group_members) > MIN_GROUP_CONSISTENCY:
                self.group_members.append(chosen_user)

    def initialise(self):
        for _ in range(NUMBER_OF_INIT_TRIES):
            chosen_users = sample(self.model.users, k=3)

            if self.calculate_consistency(chosen_users) > MIN_GROUP_CONSISTENCY:
                self.group_members.extend(chosen_users)
                break

    def step(self):
        if not self.group_members:
            self.initialise()
        elif self.update_group():  # True if group still exists
            self.search_new_members()

    def present_group(self):
        print("Group" + str(self.unique_id) + ": size=", str(len(self.group_members)), ", members=", self.group_members)
