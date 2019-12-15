import numpy as np
import random
from config import TAGS
from action_types import ACTIONS


def define_user_interests():
    exp = list(np.random.normal(0, 1, len(TAGS)))
    values = [float(value) / 3 if abs(float(value) / 3) <=
              1 else round(float(value) / 3) for value in exp]
    return {tag: values.pop() for tag in TAGS}


def define_user_actions_probabilities(exp_normalized: list):
    d = {}
    for action in ACTIONS:
        v = random.choice(exp_normalized) * 2
        if action is "react":
            v *= 1.5
        elif action is "share_post":
            v *= 0.7
        d[action] = v if abs(v) <= 1 else 1
    return d
