import random
from collections import defaultdict

from mesa import Agent
from numpy import mean

from Actions import Post, Reaction, Comment
from config import TAGS, INITIAL_RELATION_VALUE, RELATION_DECAY_PER_CYCLE, MIN_CHANCE_FOR_FRIENDS
from action_types import REACT, WRITE_COMMENT, SHARE_POST, WRITE_POST


class UserAgent(Agent):

    def __init__(self, unique_id, interests, actions_probabilities, influence, model):
        super().__init__(unique_id, model)
        self._relations = defaultdict(float)  # weights determining the relationship with users
        self._interests = interests
        self._posts = []  # written _posts
        self._performed_actions = defaultdict(int)
        self._positive_actions_by_user = {}
        self._negative_actions_by_user = {}
        self._actions_probabilities = actions_probabilities
        self._influence = influence
        self._friends = []
        self._roles = defaultdict(list)
        self._actions = {"write_comment": self.write_comment_to_post,
                         "write_post": self.write_post,
                         "react": self.react_to_post,
                         "share_post": self.share_post}
        self._action_relation_values = {
            "write_comment": 1,
            "react": 0.5,
            "share_post": 2
        }

    def get_relations(self):
        return self._relations

    def get_relation(self, user):
        if user in self._relations:
            return self._relations[user]
        else:
            return 0

    def get_number_of_friends(self):
        return len(self.friends)

    def get_number_of_neighbors_in_group(self, group):
        neighbors_count = 0
        for member in group:
            if member in self._relations.keys():
                neighbors_count += 1
        return neighbors_count

    def get_number_of_neighbors_outside_the_group(self, group):
        neighbors_count = 0
        for neighbor in self._relations.keys():
            if neighbor not in group:
                neighbors_count += 1
        return neighbors_count

    def get_influence_by_edges(self, group):
        influence = 0
        for member in group.group_members:
            if member in self._relations.keys():
                influence += self._relations[member]
        return influence
        # TODO check if self._relations contains in-edges

    def get_activity_by_edges(self, group):
        influence = 0
        for member in group.group_members:
            if member in self._relations.keys():
                influence += member.get_relations()[self]
        return influence
        # TODO check if member.get_relations()[self] contains out-edges

    def get_number_of_positive_actions(self, group):
        """Positive actions (actions performed only for users from group, all action types)"""
        for member in group.group_members:
            if member in self._positive_actions_by_user.keys():
                return self._positive_actions_by_user[member]

    def get_number_of_negative_actions(self, group):
        """Negative actions (actions performed only for users from group, all action types)"""
        for member in group.group_members:
            if member in self._negative_actions_by_user.keys():
                return self._negative_actions_by_user[member]

    def get_number_of_comments(self):
        """"Number of actions (actions performed for all users)"""
        return self._performed_actions[WRITE_COMMENT]

    def get_number_of_posts(self):
        """Number of actions (all posts added)"""
        return self._performed_actions[WRITE_POST]

    def get_number_of_shares(self):
        """Number of actions (shares performed - all users posts)"""
        return self._performed_actions[SHARE_POST]

    def get_number_of_reactions(self):
        """Number of actions (reactions performed - all users posts)"""
        return self._performed_actions[REACT]

    def add_role(self, role, group):
        self._roles[group.unique_id].append(role)

    def present_roles(self):
        print("User" + str(self.unique_id) + ": roles=", self._roles)

    def update_relation(self, user, action_type):
        self._relations[user] += self._action_relation_values[action_type]

    def get_interests(self):
        return self._interests

    @property
    def influence(self):
        return self._influence

    def get_actions_probabilities(self):
        return self._actions_probabilities

    def get_random_post(self):
        if not len(self._posts):
            return None
        return random.choice(self._posts)

    def decrease_connections(self):
        for user in self._relations.keys():
            self._relations[user] *= RELATION_DECAY_PER_CYCLE

    def add_friend(self, user):
        self._friends.append(user)
        self._relations[user] = INITIAL_RELATION_VALUE

    def add_random_friends(self, num_of_friends):
        new_friends = random.choices(self.model.users, k=num_of_friends)
        for friend in new_friends:
            self.try_to_become_friends(friend)

    @property
    def performed_actions(self):
        return self._performed_actions

    @property
    def posts(self):
        return self._posts

    @property
    def friends(self):
        return self._friends

    def try_to_become_friends(self, user):
        if user in self._friends:
            return
        mutual_friends = set(self._friends).intersection(user.friends)
        mutual_length = len(mutual_friends)
        mutual_friends_addition = mutual_length * 0.01 + MIN_CHANCE_FOR_FRIENDS
        if mutual_friends_addition > random.random():
            self.add_friend(user)
            user.add_friend(self)

    def expand_influence(self):
        """ Expands user influence (how big his reach is outside his friend list) based
            Based on self._influence value. Essentially it adds friends in ONE way only.
            Meaning they can be reach but they cannot be reached.
        """
        user_reach = int(len(self.model.users) * self._influence)
        # print(f'User reach of {self._influence} is {user_reach} / {len(self.model.users)}')
        for user in random.sample(self.model.users, user_reach):
            self.add_friend(user)

    def write_comment_to_post(self):
        """Randomly go through friends and choose random post to comment
           Add Comment to post with unique_id and interests for first tag from post
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            attitude = self._interests[random.choice(post.tags)]
            self.update_positive_and_negative_actions(friend, attitude)
            comment = Comment(attitude, self.unique_id)
            post.add_comment(comment)
            friend.update_relation(self, WRITE_COMMENT)
            friend.append_comment(post, comment)
            # self.update_relation(friend, WRITE_COMMENT)
            break


    def write_post(self, tags=None, user=None):
        if tags is None:
            tags = random.choices(TAGS, k=random.randint(1, len(TAGS)))
            attitude = mean([self._interests[tag] for tag in tags])
            self.update_positive_and_negative_actions(user, attitude)
        attitude = mean([self._interests[tag] for tag in tags])
        new_post = Post(attitude=attitude, author=self, tags=tags)
        self._posts.append(new_post)

    def update_positive_and_negative_actions(self, user, attitude):
        if user not in self._positive_actions_by_user:
            self._positive_actions_by_user[user] = 0
            self._negative_actions_by_user[user] = 0
        if attitude >= 0:
            self._positive_actions_by_user[user] += 1
        else:
            self._negative_actions_by_user[user] += 1

    def react_to_post(self):
        """Randomly go through friends and choose random post to react
           Add Reaction to post with unique_id and interests for first tag from post
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            attitude = self._interests[random.choice(post.tags)]
            self.update_positive_and_negative_actions(friend, attitude)
            reaction = Reaction(attitude, self.unique_id)
            post.add_reaction(reaction)
            friend.update_relation(self, REACT)
            friend.append_reaction(post, reaction)
            # self.update_relation(friend, REACT)
            break


    def share_post(self):
        """Randomly go through friends and choose random post to share
           Add shared to its own list of posts
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            # self._posts.append(post)
            self.write_post(post.tags, friend)
            friend.update_relation(self, SHARE_POST)
            friend.append_share(post, user=self)
            # self.update_relation(friend, SHARE_POST)
            break

    def append_reaction(self, post, reaction):
        self._posts[self.get_post_idx(post)].add_reaction(reaction)

    def append_comment(self, post, comment):
        self._posts[self.get_post_idx(post)].add_comment(comment)

    def append_share(self, post, user):
        self._posts[self.get_post_idx(post)].add_shared(user)

    def get_post_idx(self, post):
        return self._posts.index(post)

    def step(self):
        actions: list = list(self._actions_probabilities)

        for action in random.sample(actions, len(actions)):
            probability = self._actions_probabilities[action]
            r = random.random()
            if r <= probability:
                self._actions[action]()
                self._performed_actions[action] += 1

        for user in self.model.schedule.agents:
            self.try_to_become_friends(user)
        self.decrease_connections()
