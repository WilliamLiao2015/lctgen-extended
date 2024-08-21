import math

import numpy as np
import matplotlib.pyplot as plt

from utils.geometry import compute_magnitude


def visualize_minimum_speed_rate(data, agents, t, label_y = 50):
    ax = plt.gca()

    ax.text(-60, label_y, f"Minimum speed rate: {evaluate_minimum_speed_rate(data, agents, t):.2%}", fontsize=10, color="black")

    return ax


def evaluate_minimum_speed_rate(data, agents, t, log=False):
    """Minimum speed rate: {result:.2%}"""

    speeds = []
    min_speed = np.inf

    for i, agent in enumerate(agents[t]):
        position = agent.position[0]
        velocity = agent.velocity[0]
        if abs(position[0]) > 45 or abs(position[1]) > 45: continue
        if t == 0:
            angle = math.atan2(velocity[1], velocity[0]) / math.pi * 180
            speed = compute_magnitude(*velocity)
        else:
            px, py = agents[t - 1][i].position[0]
            dx, dy = position[1] - py, position[0] - px
            angle = math.atan2(dx, dy) / math.pi * 180
            # speed = abs(velocity)
            speed = compute_magnitude(dx, dy) * 10 # Maybe FPS?
        if min_speed > speed: min_speed = speed
        speeds.append(speed)

    average_speed = np.mean(speeds)
    min_speed_rate = (min_speed / average_speed) if average_speed > 0 else 0.0

    if log:
        print(f"Timestep {t + 1}:")
        print(f"Minimum speed rate: {min_speed_rate:.2%}")

    return min_speed_rate
