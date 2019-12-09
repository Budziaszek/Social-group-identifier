from model import SiteModel
# import matplotlib.pyplot as plt

number_of_users = 3
number_of_steps = 1


model = SiteModel(number_of_users)
for _ in range(number_of_steps):
    model.step()

# agent_comments = [a.comments for a in model.schedule.agents]
# plt.hist(agent_comments)
# plt.show()

