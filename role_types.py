roles_influence = ["Spamer", "Celebryta", "Popularny", "Nowy"]
roles_neighbors = ["Koncentrator", "Pośrednik", "Wszędobylski"]
roles_attitude = ["Narzekacz", "Komplemenciarz", "Neutralny_Zbalansowany"]
roles_activities = ["Lurker", "Komentujący", "Piszący", "Udostępniający", "Zbalansowany"]

roles = []
roles.extend(roles_influence)
roles.extend(roles_neighbors)
roles.extend(roles_activities)
roles.extend(roles_attitude)


def get_name(check_roles):
    if check_roles == roles_influence:
        return "Influence"
    elif check_roles == roles_neighbors:
        return "Neighbors"
    elif check_roles == roles_attitude:
        return "Attitude"
    else:
        return "Activities"
