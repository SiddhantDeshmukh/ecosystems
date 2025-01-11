import random
import numpy as np
from typing import List


def generate_from_list(lst: List[str],
                       chance: float) -> str:
    # Generate a an elememt from "lst" based on "chance", else return ""
    return random.choice(lst) if random.random() <= chance else ""


def generate_potential_pair(lst: List[str],
                            secondary_chance: float) -> List[str]:
    # Pick one or two animal families from the list
    if random.random() <= secondary_chance:
        return random.sample(lst, 2)
    else:
        return [random.choice(lst), ""]


def weighted_randint(a: int, b: int) -> int:
    # Generates random number between 'a' and 'b' inclusive with weighting
    # so higher numbers are less likely
    choices = list(range(a, b+1))
    probs = 1 / (2*np.array(choices))
    # Normalize
    probs /= np.sum(probs)
    return np.random.choice(choices, p=probs)
