from imports.packages import plt


def draw(center, agents, traj=None, other=None, edge=None, heat_map=False):
    """
    - V1: red (ego car)
    - V2: blue
    - V3: orange
    - V4: green
    - V5: purple
    - V6: brown
    - V7: pink
    - V8: gray
    - V9: olive
    - V10: cyan
    - V11 (V2): blue
    - V12 (V3): orange
    - V13 (V4): green
    - ...
    """
    ax = plt.gca()
    plt.axis('equal')

    colors = ['tab:red', 'tab:blue', 'tab:orange', 'tab:green', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    lane_color = 'black'
    alpha = 0.12
    linewidth = 3

    if heat_map:
        lane_color = 'white'
        alpha = 0.2
        linewidth = 6

    ax.axis('off')

    for j in range(center.shape[0]):
        traf_state = center[j, -1]

        x0, y0, x1, y1, = center[j, :4]

        if x0 == 0: break
        ax.plot((x0, x1), (y0, y1), '--', color=lane_color, linewidth=1, alpha=0.2)

        if traf_state == 1:
            color = 'red'
            ax.plot((x0, x1), (y0, y1), color=color, alpha=alpha, linewidth=linewidth, zorder=5000)
        elif traf_state == 2:
            color = 'yellow'
            ax.plot((x0, x1), (y0, y1), color=color, alpha=alpha, linewidth=linewidth, zorder=5000)
        elif traf_state == 3:
            color = 'green'
            ax.plot((x0, x1), (y0, y1), color=color, alpha=alpha, linewidth=linewidth, zorder=5000)

    if edge is not None:
        for j in range(len(edge)):

            # if lane[j, k, -1] == 0: continue
            x0, y0, x1, y1, = edge[j, :4]
            if x0 == 0: break
            ax.plot((x0, x1), (y0, y1), lane_color, linewidth=1.5)
            # ax.arrow(x0, y0, x1-x0, y1-y0,head_width=1.5,head_length=0.75,width = 0.1)

    if other is not None:
        for j in range(len(other)):

            # if lane[j, k, -1] == 0: continue
            x0, y0, x1, y1, = other[j, :4]
            if x0 == 0: break
            ax.plot((x0, x1), (y0, y1), lane_color, linewidth=0.7, alpha=0.9)

    for i in range(len(agents)):
        agent_position = agents[i].position[0]
        if abs(agent_position[0]) > 45 or abs(agent_position[1]) > 45: continue

        # if i in collide: continue
        if i == 0:
            col = colors[0]
        else:
            ind = (i-1) % 9 + 1
            col = colors[ind]
            if traj is not None:
                traj_i = traj[:, i]
                len_t = traj_i.shape[0] - 1
                for j in range(len_t):
                    x0, y0 = traj_i[j]
                    x1, y1 = traj_i[j + 1]

                    if abs(x0) < 60 and abs(y0) < 60 and abs(x1) < 60 and abs(y1) < 60:
                        ax.plot((x0, x1), (y0, y1), '-', color=col, linewidth=1.8, marker='.', markersize=3)

        agent = agents[i]
        rect = agent.get_rect()[0]
        rect = plt.Polygon(rect, edgecolor='black', facecolor=col, linewidth=0.5, zorder=10000)
        ax.add_patch(rect)

    # ax.set_facecolor('black')
    plt.autoscale()
    plt.xlim([-60, 60])
    plt.ylim([-60, 60])


def visualize(data, agents, t = 0):
    center = data["center"][0].cpu().numpy()
    bound = data["bound"][0].cpu().numpy()
    rest = data["rest"][0].cpu().numpy()

    draw(center, agents[t], other=rest, edge=bound)

    ax = plt.gca()
    ax.text(-60, 60, f"Timestep {t + 1}", fontsize=12, color="black", weight="bold")

    return ax
