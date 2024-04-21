from imports.packages import plt, LineString


def visualize_road_collision_rate(data, agents, t = 0, label_y = 50):
    ax = plt.gca()

    for i, agent in enumerate(agents[t]):
        position = agent.position[0]
        if abs(position[0]) > 45 or abs(position[1]) > 45: continue
        car = agent.get_polygon()[0]
        for lane in data["bound"][0]:
            x1, y1, x2, y2 = lane[:4]
            if x1 == 0: break
            lane = LineString(((x1, y1), (x2, y2)))
            if car.intersects(lane):
                ax.plot((x1, x2), (y1, y2), c="red", linewidth=1)

    ax.text(-60, label_y, f"Road collision rate: {evaluate_road_collision_rate(data, agents, t):.2%}", fontsize=10, color="black")

    return ax


def evaluate_road_collision_rate(data, agents, t, log=False):
    """Road collision rate: {result:.2%}"""

    touch_cnt = 0

    for i, agent in enumerate(agents[t]):
        position = agent.position[0]
        if abs(position[0]) > 45 or abs(position[1]) > 45: continue
        car = agent.get_polygon()[0]
        for lane in data["bound"][0]:
            x1, y1, x2, y2 = lane[:4]
            if x1 == 0: break
            lane = LineString(((x1, y1), (x2, y2)))
            if car.intersects(lane):
                if log: print(f"V{i + 1} collides with lane")
                touch_cnt += 1
                break # each car collides at most once

    road_collision_rate = (touch_cnt / len(agents[t])) if len(agents[t]) > 0 else 0.0

    if log:
        print(f"Timestep {t + 1}:")
        print(f"Road collision rate: {road_collision_rate:.2%}")

    return road_collision_rate
