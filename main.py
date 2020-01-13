from role_types import roles
from model import SiteModel
from config import NUMBER_OF_STEPS, NUMBER_OF_USERS

model = SiteModel(NUMBER_OF_USERS)

for _ in range(NUMBER_OF_STEPS):
    model.step()

groups = []  # TODO create groups

for _ in range(len(roles)):
    model.assign_roles_init(groups)
