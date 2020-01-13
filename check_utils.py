import collections
import random
import functools
import operator
import numpy as np
import matplotlib.pyplot as plt

from action_types import ACTIONS
from config import TAGS


# check_influence_distribution()
# check_total_tags_distribution()
# check_random_user_tags_distribution(2)
# check_distribution_by_tag()
# check__total_user_actions_probabilities()
# plot_data_lengths(data=[len(a.posts) for a in model.schedule.agents],
#                   title="Number of posts")
# plot_dictionary(dicts=[a.performed_actions for a in model.schedule.agents],
#                 title="Performed actions")
# plot_data_lengths(data=[len(a.friends) for a in model.schedule.agents],
#                   title="Total friends", not_too_long_flag=False,
#                   xlabel="Number of friends for each user",
#                   ylabel="Number of users with y friends")

def check_influence_distribution(model):
    agent_data = [a.get_influence() for a in model.schedule.agents]
    plt.hist(agent_data)
    plt.title("User influence")
    plt.show()


def check_total_tags_distribution(model):
    agents_dicts = [a.get_interests() for a in model.schedule.agents]
    agents_dicts_sum = {}
    for tag in TAGS:
        agents_dicts_sum[tag] = sum(abs(d[tag]) for d in agents_dicts)
    plt.title("Sum of tag interests (abs)")
    plt.bar(agents_dicts_sum.keys(), agents_dicts_sum.values())
    plt.show()


def check_distribution_by_tag(model):
    agents_dicts = [a.get_interests() for a in model.schedule.agents]
    dict_all = collections.defaultdict(list)
    for tag in TAGS:
        dict_all[tag] = []
        for d in agents_dicts:
            dict_all[tag].append(d[tag])
        plt.title(tag)
        plt.hist(dict_all[tag])
        plt.show()


def check_random_user_tags_distribution(model, number_of_users_to_display):
    for _ in range(number_of_users_to_display):
        agent_dict = random.choice(model.schedule.agents).get_interests()
        plt.bar(agent_dict.keys(), agent_dict.values())
        plt.title("Random user interests")
        plt.show()


def check__total_user_actions_probabilities(model):
    agents_dicts = [a.get_actions_probabilities()
                    for a in model.schedule.agents]
    dict_all = collections.defaultdict(list)
    for action in ACTIONS:
        dict_all[action] = []
        for d in agents_dicts:
            dict_all[action].append(d[action])
        plt.title(action)
        plt.hist(dict_all[action])
        plt.show()


def check_number_of_friends_distribution(model):
    agent_data = [a.get_number_of_friends() for a in model.schedule.agents]
    plt.hist(agent_data)
    plt.title("Number of friends")
    plt.show()


# check_number_of_friends_distribution()
def plot_data_lengths(data, title, not_too_long_flag=True, xlabel="", ylabel=""):
    bins = np.arange(0, max(data) + 1.5) - 0.5
    fig, ax = plt.subplots()
    plt.title(title)
    _ = ax.hist(data, bins)
    if not_too_long_flag:
        ax.set_xticks(bins + 0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_dictionary(dicts, title):
    plt.title(title)
    result = dict(functools.reduce(operator.add,
                                   map(collections.Counter, dicts)))
    lists = sorted(result.items())
    x, y = zip(*lists)
    plt.bar(x, y)
    plt.show()
