from user_agent import UserAgent
import matplotlib.pyplot as plt


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
    """Plot size of the number of post writter for user 0 throughout simulation"""
    """plt.plot must be called after"""
    number_of_post_written = model.data_collector.get_agent_vars_dataframe()

    plt.figure()
    plt.title('Number of post written throughout whole program for agent 0')
    plt.xlabel("Iterations")
    plt.ylabel("Number of post written")
    one_agent_wealth = number_of_post_written.xs(0, level="AgentID")
    one_agent_wealth.Post_written.plot()
