from UserAgent import UserAgent


def get_number_of_reactions(agent):
    if agent is UserAgent:
        return agent.get_number_of_reactions()
    else:
        return None


def biggest_group(model):
    biggest = 0
    for gr in model.groups:
        if gr.size > biggest:
            biggest = gr.size
    return biggest
