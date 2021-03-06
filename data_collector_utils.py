from collections import defaultdict

from user_agent import UserAgent
import matplotlib.pyplot as plt
from role_types import get_name, roles_influence, roles_neighbors, roles_activities, roles_attitude
from config import MAX_GROUP_MEMBERS, CURR_MODE, MODE_WITH_NEGOTIATIONS


def get_number_of_groups(model):
    """Get number of non-empty groups"""
    return sum(map(lambda x: int(x.size > 0), model.groups))


def get_number_of_post_written(agent):
    if type(agent) is UserAgent:
        return agent.get_number_of_posts()
    else:
        return None


def biggest_group(model):
    biggest = 0
    for gr in model.groups:
        if gr.size > biggest:
            biggest = gr.size
    return biggest


def group_size_dist(model):
    """Collects data about distribution of group sizes divided into no_bars=10 ranges"""
    no_bars = 5
    sizes = [0 for _ in range(no_bars)]
    for gr in model.groups:
        if gr.is_empty:
            continue

        index = int(gr.size / (MAX_GROUP_MEMBERS + 1) * no_bars)
        sizes[index] += 1
    return sizes


def plot_stats(model):
    """Main plot function, plot all stats"""
    plot_biggest_group(model)
    plot_number_of_groups_during_simulation(model)
    plot_group_size_distribution(model)
    plot_post_written(model)
    plot_roles_histogram(model)
    if CURR_MODE is MODE_WITH_NEGOTIATIONS:
        plot_roles_negotiations_histogram(model)
    plot_roles_combinations_histogram(model)
    plot_roles_changes(model)
    plot_roles_changes_histogram(model)
    plt.show()


def plot_biggest_group(model):
    """Plot size of the biggest group throughout simulation"""
    """plt.plot must be called after"""
    biggest_group = model.data_group_collector.get_model_vars_dataframe()
    biggest_group_plot = biggest_group["biggestGroup"].plot()
    biggest_group_plot.set_xlabel("Iterations")
    biggest_group_plot.set_ylabel("Size of the biggest group")
    biggest_group_plot.set_title("Size of the biggest group throughout simulation")


def plot_post_written(model):
    """Plot size of the number of post written for user 0 throughout simulation"""
    """plt.plot must be called after"""
    number_of_post_written = model.data_collector.get_agent_vars_dataframe()

    plt.figure()
    plt.title('Number of post written throughout whole program for agent 0')
    plt.xlabel("Iterations")
    plt.ylabel("Number of post written")
    one_agent_wealth = number_of_post_written.xs(0, level="AgentID")
    one_agent_wealth.Post_written.plot()


def plot_roles_histogram(model):
    for type_of_group in [roles_influence, roles_neighbors, roles_activities, roles_attitude]:
        roles_dict = {}
        for user in model.users:
            user.fill_roles(roles_dict, type_of_group)
        plt.figure()
        plt.title('Histogram of roles from {}'.format(get_name(type_of_group)))
        plt.bar(roles_dict.keys(), roles_dict.values(), width=1, color='g')


def plot_roles_negotiations_histogram(model):
    for type_of_group in [roles_influence, roles_neighbors, roles_activities, roles_attitude]:
        plt.figure()
        plt.title('Histogram of negotiations - roles from {}'.format(get_name(type_of_group)))
        plt.bar([key[0][0:3] + "-" + key[1][0:3] for key in model.negotiations[get_name(type_of_group)].keys()],
                model.negotiations[get_name(type_of_group)].values(), width=1, color='g')
        plt.xticks(rotation=90)


def plot_roles_combinations_histogram(model):
    plt.figure()
    plt.title('Histogram of roles combinations (only existing ones)')
    dictionary = model.check_roles_combinations()
    new_dictionary = {}
    for key in dictionary:
        if dictionary[key] != 0:
            new_key = key[0][0:3] + '-' + key[1][0:3]
            new_dictionary[new_key] = dictionary[key]
    plt.bar(new_dictionary.keys(), new_dictionary.values(), width=1, color='g')
    plt.xticks(rotation=90)


def plot_number_of_groups_during_simulation(model):
    data_group_data = model.data_group_collector.get_model_vars_dataframe()
    group_sizes = data_group_data["number_of_groups"]
    plt.figure()
    plt.title('Number of groups during simulation')
    plt.xlabel('Iterations')
    plt.ylabel('Number of groups')
    plt.plot(group_sizes.tolist())


def plot_group_size_distribution(model):
    data_group_data = model.data_group_collector.get_model_vars_dataframe()
    group_sizes = data_group_data["groupSizeDistribution"]
    plt.figure()
    plt.title('Group size distribution during simulation')
    plt.xlabel('Iterations')
    plt.ylabel('Number of groups')
    group_sizes = list(map(list, zip(*group_sizes)))
    for i, size in enumerate(group_sizes):
        plt.plot(size, label=f'{int(i/len(group_sizes)*100)} to {int((i + 1)/len(group_sizes)*100)}%')
    plt.legend()


def plot_roles_changes(model):
    for type_of_group in [roles_influence, roles_neighbors, roles_activities, roles_attitude]:
        plt.figure()
        for role in type_of_group:
            plt.plot(model.roles_count[role], label=role)
        plt.title('Change of roles over time{}'.format(get_name(type_of_group)))
        plt.xlabel('Iterations')
        plt.ylabel('% of role')
        plt.legend()


def plot_roles_changes_histogram(model):
    plt.figure()
    plt.title('Histogram of roles changes')
    dictionary = model.role_changes_from
    print(dictionary)
    plt.bar(dictionary.keys(), dictionary.values(), width=1, color='g')
    plt.xticks(rotation=90)


