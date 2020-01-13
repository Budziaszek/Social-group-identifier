from mesa import Agent


class RoleAgent(Agent):
    groups = []
    WITH_NEGOTIATIONS = "negotiations"
    WITHOUT_NEGOTIATIONS = "no_negotiations"
    mode = WITHOUT_NEGOTIATIONS

    def __init__(self, unique_id, role, model):
        super().__init__(unique_id, model)
        self.role = role
        self.users_assigned = []

    def determine_users_roles(self):
        for group in self.groups:
            for user in group:
                self.check_criteria(user, group)

    def check_criteria(self, user, group):
        pass

    def negotiate(self):
        pass
