import random
from mesa import Agent
from copy import deepcopy
from Actions import Post, Reaction, Comment
from config import TAGS, INITIAL_RELATION_VALUE, RELATION_DECAY_PER_CYCLE, MIN_CHANCE_FOR_FRIENDS
from action_types import REACT, WRITE_COMMENT, SHARE_POST


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
        self._action_relation_values = {
            "write_comment": 1,
            "react": 0.5,
            "share_post": 2
        }

    def get_number_of_friends(self):
        return len(self.friends)

    def update_relation(self, user, action_type):
        self._relations[user] += self._action_relation_values[action_type]

    def get_interests(self):
        return self._interests

    def get_influence(self):
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

    def write_comment_to_post(self):
        """Randomly go through friends and choose random post to comment
           Add Comment to post with unique_id and interests for first tag from post
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            post.add_comment(
                Comment(self._interests[post.tags[0]], self.unique_id))
            friend.update_relation(self, WRITE_COMMENT)
            self.update_relation(friend, WRITE_COMMENT)
            break

        print(self.unique_id, "write comment")

    def write_post(self):
        # TODO select topics, send to _friends and to some random users if _influence is high enough
        #   post is sent to everyone if user _influence is equal to 1
        #   post is sent to half of users if user _influence is equal to 0.5 etc
        new_post = Post(attitude=['?'], author=self,
                        tags=random.choices(TAGS, k=random.randint(1, len(
                            TAGS))))  # TODO: Random tags, what about attidute?
        # TODO I think attutude can by calculated from interests (tags)
        #   eg. if tags are dog, cat and dog:1, cat:0.5 attitude = ceil((1 + 0.5)/2)
        self._posts.append(new_post)
        print(self.unique_id, "write post")

    def react_to_post(self):
        """Randomly go through friends and choose random post to react
           Add Reaction to post with unique_id and interests for first tag from post
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            post.add_reaction(
                Reaction(self._interests[post.tags[0]], self.unique_id))
            friend.update_relation(self, REACT)
            self.update_relation(friend, REACT)
            break

        print(self.unique_id, "react")

    def share_post(self):
        """Randomly go through friends and choose random post to share
           Add shared to its own list of posts
           Update relations between friends
        """
        for friend in random.sample(self._friends, len(self._friends)):
            post: Post = friend.get_random_post()
            if not post:
                continue
            self._posts.append(post)
            friend.update_relation(self, SHARE_POST)
            self.update_relation(friend, SHARE_POST)
            break

        print(self.unique_id, "share post")

    def append_react(self, post_id, reaction):
        self._posts[post_id].add_reaction(reaction)

    def append_comment(self, post_id, comment):
        self._posts[post_id].add_comment(comment)

    def append_observer(self, post_id, user):
        self._posts[post_id].add_observer(user)

    def step(self):
        actions: list = list(self._actions_probabilities)

        for action in random.sample(actions, len(actions)):
            probability = self._actions_probabilities[action]
            r = random.random()
            if r <= probability:
                self._actions[action]()

        for user in self.model.schedule.agents:
            self.try_to_become_friends(user)
        self.decrease_connections()
