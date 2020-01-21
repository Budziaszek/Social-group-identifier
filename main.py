import matplotlib.pyplot as plt
from model import SiteModel
from config import NUMBER_OF_STEPS, NUMBER_OF_USERS, MAX_NUMBER_OF_GROUPS, NUMBER_OG_GROUP_STEPS

model = SiteModel(NUMBER_OF_USERS)

print("______________SIMULATION______________")

for _ in range(NUMBER_OF_STEPS):
    model.step()

print("________________GROUPS________________")

model.create_groups(MAX_NUMBER_OF_GROUPS)
for _ in range(NUMBER_OG_GROUP_STEPS):
    model.step_groups()
for group in model.groups:
    group.present_group()

print("________________ROLES_________________")
model.assign_roles_init(model.groups)
for user in model.users:
    user.present_roles()

biggest_group = model.datacollector.get_model_vars_dataframe()
biggest_group.plot()

plt.show()

number_of_post_written = model.datacollector.get_agent_vars_dataframe()
print(number_of_post_written)
