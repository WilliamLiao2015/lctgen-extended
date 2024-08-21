import math
import itertools

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from shapely.geometry import Polygon

from utils.geometry import compute_magnitude


vision = 60
vis_range = 60


def get_sector(center, radius, start_angle, end_angle, steps=180):
    def polar_point(origin_point, angle,  distance):
        return [origin_point[0] + math.cos(math.radians(angle)) * distance, origin_point[1] + math.sin(math.radians(angle)) * distance]

    step_angle_width = (end_angle - start_angle) / steps
    sector_width = (end_angle - start_angle)
    segment_vertices = []

    segment_vertices.append(polar_point(center, 0,0))
    segment_vertices.append(polar_point(center, start_angle, radius))

    for z in range(1, steps):
        segment_vertices.append((polar_point(center, start_angle + z * step_angle_width,radius)))
    segment_vertices.append(polar_point(center, start_angle + sector_width,radius))
    segment_vertices.append(polar_point(center, 0,0))

    return Polygon(segment_vertices)


def visualize_overlapped_area_rate(data, agents, t = 0, label_y = 50):
    ax = plt.gca()

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
        ax.add_artist(Wedge(position, speed, angle - vision / 2, angle + vision / 2, color="red", alpha=0.3))

    ax.text(-60, label_y, f"Overlapped area rate: {evaluate_overlapped_area_rate(data, agents, t):.2%}", fontsize=10, color="black")

    return ax


def evaluate_overlapped_area_rate(data, agents, t, log=False):
    """Overlapped area rate: {result:.2%}"""

    overlapped_area = 0
    sectors = []

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
        sector = get_sector(position, speed, angle - vision / 2, angle + vision / 2)
        sectors.append([i + 1, agent.get_polygon()[0], sector])

    total_area = 0

    if log: print(f"Timestep {t + 1}:")
    for (i1, c1, s1), (i2, c2, s2) in itertools.combinations(sectors, 2):
        s1 = s1.union(c1)
        s2 = s2.union(c2)
        area = s1.intersection(s2).area
        sector_area = s1.area + s2.area
        total_area += sector_area
        if area == 0: continue
        overlapped_area += area * 2
        if log: print(f"V{i1} and V{i2} overlapped, area rate: {area / sector_area:.2%}")

    overlapped_area_rate = (overlapped_area / total_area) if total_area > 0 else 0.0

    if log: print(f"Total overlapped area rate: {overlapped_area_rate:.2%}")

    return overlapped_area_rate
