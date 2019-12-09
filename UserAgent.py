from random import random

from mesa import Agent


class UserAgent(Agent):

    def __init__(self, unique_id, interests, actions_probabilities, influence, model):
        super().__init__(unique_id, model)
        self._relations = {}  # weights determining the relationship with users
        self._interests = interests
        self._posts = []  # written _posts
        self._performed_actions = []
        self._actions_probabilities = actions_probabilities
        self._influence = influence
        self._friends = []
        self._actions = {"write_comment": self.write_comment_to_post,
                         "write_post": self.write_post,
                         "react": self.react_to_post,
                         "share_post": self.share_post}

    def get_interests(self):
        return self._interests

    def get_influence(self):
        return self._influence

    def get_actions_probabilities(self):
        return self._actions_probabilities

    def update_relation(self, user):
        # TODO Update relation with user
        pass

    def decrease_connections(self):
        # TODO Update _relations (with each user) - multiply each by 0.9
        pass

    def add_friend(self, user):
        # TODO add to _friends, create relation
        pass

    def add_random_friends(self, num_of_friends):
        # TODO add randomly some _friends, use add_friend
        pass

    def try_to_become_friends(self, user):
        # TODO check if user become friend with given user, use add_friend
        #   gaining new _friends depends on mutual _friends,
        #   probability of becoming _friends is always higher than 0
        pass

    def write_comment_to_post(self):
        # TODO add comment to selected post, update relation
        print(self.unique_id, "write comment")

    def write_post(self):
        # TODO select topics, send to _friends and to some random users if _influence is high enough
        #   post is sent to everyone if user _influence is equal to 1
        #   post is sent to half of users if user _influence is equal to 0.5 etc
        print(self.unique_id, "write post")

    def react_to_post(self):
        # TODO react to selected post, update relation
        print(self.unique_id, "react")

    def share_post(self):
        # TODO react to selected post, update relation
        print(self.unique_id, "share post")

    def append_react(self, post_id):
        # TODO someone reacted post
        pass

    def append_comment(self, post_id):
        # TODO someone commented post
        pass

    def append_share(self, post_id):
        # TODO someone shared post
        pass

    def step(self):
        for action in self._actions_probabilities:
            probability = self._actions_probabilities[action]
            r = random()
            if r <= probability:
                self._actions[action]()
        for user in self.model.schedule.agents:
            self.try_to_become_friends(user)
        self.decrease_connections()
