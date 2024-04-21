from imports.system import itertools
from imports.packages import plt


def visualize_car_collision_rate(data, agents, t, label_y = 50):
    ax = plt.gca()

    for (i1, a1), (i2, a2) in itertools.combinations(enumerate(agents[t]), 2):
        p1 = a1.position[0]
        p2 = a2.position[0]
        if abs(p1[0]) > 45 or abs(p1[1]) > 45 or abs(p2[0]) > 45 or abs(p2[1]) > 45: continue
        c1 = a1.get_polygon()[0]
        c2 = a2.get_polygon()[0]
        if c1.intersects(c2):
            ax.add_patch(plt.Circle(p1, 10, color="r", alpha=0.3))
            ax.add_patch(plt.Circle(p2, 10, color="r", alpha=0.3))

    ax.text(-60, label_y, f"Car collision rate: {evaluate_car_collision_rate(data, agents, t):.2%}", fontsize=10, color="black")

    return ax


def evaluate_car_collision_rate(data, agents, t, log=False):
    """Car collision rate: {result:.2%}"""

    collisions = 0

    for (i1, a1), (i2, a2) in itertools.combinations(enumerate(agents[t]), 2):
        p1 = a1.position[0]
        p2 = a2.position[0]
        if abs(p1[0]) > 45 or abs(p1[1]) > 45 or abs(p2[0]) > 45 or abs(p2[1]) > 45: continue
        c1 = a1.get_polygon()[0]
        c2 = a2.get_polygon()[0]
        if c1.intersects(c2):
            if log: print(f"V{i1 + 1} and V{i2 + 1} crashed")
            collisions += 2

    car_collision_rate = (collisions / len(agents[t])) if len(agents[t]) > 0 else 0.0

    if log:
        print(f"Timestep {t + 1}:")
        print(f"Car collision rate: {car_collision_rate:.2%}")

    return car_collision_rate
