from model import SiteModel
from config import NUMBER_OF_SIMULATION_STEPS, NUMBER_OF_USERS, MAX_NUMBER_OF_GROUPS, NUMBER_OF_GROUP_STEPS, \
    NUMBER_OF_STEPS
from data_collector_utils import plot_stats

model = SiteModel(NUMBER_OF_USERS)

for step in range(NUMBER_OF_STEPS):
    for user in model.users:
        user.reset()

    print("_____________SIMULATION_" + str(step) + "_____________")
    for i in range(NUMBER_OF_SIMULATION_STEPS):
        model.step()
        print(f"\rCurrent progress {(i + 1) / NUMBER_OF_SIMULATION_STEPS * 100}%..", end="")

    print(" Simulation finished!")
    print("________________GROUPS________________")

    model.create_groups(MAX_NUMBER_OF_GROUPS)
    for _ in range(NUMBER_OF_GROUP_STEPS):
        model.step_groups()
    # for group in model.groups:
    #     group.present_group()
    print("Groups created")

    print("________________ROLES_________________")
    model.assign_roles_init(model.groups)
    # for user in model.users:
    #     user.present_roles()
    print("Roles assigned")

plot_stats(model)

