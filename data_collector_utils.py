from user_agent import UserAgent


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
