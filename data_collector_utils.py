from user_agent import UserAgent
import matplotlib.pyplot as plt
from role_types import get_name, roles_influence, roles_neighbors, roles_activities, roles_attitude


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


def plot_stats(model):
    """Main plot function, plot all stats"""
    plot_biggest_group(model)
    plot_post_written(model)
    plot_roles_histogram(model)
    plot_roles_negotiations_histogram(model)
    plot_roles_combinations_histogram(model)
    plt.show()


def plot_biggest_group(model):
    """Plot size of the biggest group throughout simulation"""
    """plt.plot must be called after"""
    biggest_group = model.data_group_collector.get_model_vars_dataframe()
    biggest_group_plot = biggest_group.plot()
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
        plt.bar([key[0] + "-" + key[1] for key in model.negotiations[get_name(type_of_group)].keys()],
                model.negotiations[get_name(type_of_group)].values(), width=1, color='g')


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
