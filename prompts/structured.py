import random


# "a T-intersection", "a roundabout"
roads = [
    {
        "name": "a two-way intersection",
        "actions": [0, 1, 2, 3, 4, 5, 6, 7]
    },
    {
        "name": "a four-way intersection",
        "actions": [0, 1, 2, 3, 4, 5, 6, 7]
    },
    {
        "name": "a freeway",
        "actions": [0, 2, 3, 4, 5, 6]
    }
]

actions = ["stop", "turn left", "change to left lane", "decelerate", "keep speed", "accelerate", "change to right lane", "turn right"]

scenarios = [
    {
        "type": "rear-end collision",
        "functional": "V1 goes straight and collides with V2 while V2 turns left",
        "template": "{n1} collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [4, 5]
                },
                {
                    "name": "n2",
                    "actions": [1]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "turning collision",
        "functional": "V1 turns right and bumps into V2.",
        "template": "{n1} bumps into {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [7]
                },
                {
                    "name": "n2",
                    "actions": [0, 1, 3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "head-side collision",
        "functional": "V1 is travelling straight to the south in the intersection when V2 collides it straight from the east.",
        "template": "{n1} bumps into {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [3, 4, 5]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "side-side collision",
        "functional": "V1 collides with V2 while V1 changes to left lane",
        "template": "{n1} collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [2]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    { # assumption: left-hand driving countries (TW, US, etc.)
        "type": "head-head collision",
        "functional": "V1 drives to the opposite lane and crashes V2 while V2 goes straight",
        "template": "{n1} drives to the opposite lane and crashes {n2}, {others}, on {road}",
        "abstract": {
            "roads": [0, 1, 2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [2]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "rear-end collision",
        "functional": "V1 decelerates on the freeway and V2 rear-ends it.",
        "template": "{n1} is rear-ended by {n2}, {others}, at {road}",
        "abstract": {
            "roads": [2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [3]
                },
                {
                    "name": "n2",
                    "actions": [4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "turning collision",
        "functional": "V1 is turning right at a two-way intersection when V2, coming from the opposite direction, turns left and collides with V1.",
        "template": "{n1} collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [7]
                },
                {
                    "name": "n2",
                    "actions": [1]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "head-on collision",
        "functional": "V1 is traveling north in its lane when V2 traveling south crosses into V1's lane and collides head-on.",
        "template": "{n1} collides head-on with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [4]
                },
                {
                    "name": "n2",
                    "actions": [1, 2]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "rear-end collision",
        "functional": "V1 is decelerating to stop at a red light when V2 fails to stop in time and crashes into V1 from behind.",
        "template": "{n1} is hit by {n2} from behind, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [0, 3]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "merging collision",
        "functional": "V1 merges onto a freeway and collides with V2 already traveling on the freeway.",
        "template": "{n1} merges onto the freeway and collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [2, 5]
                },
                {
                    "name": "n2",
                    "actions": [4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "U-turn collision",
        "functional": "V1 makes a U-turn at an intersection and collides with V2 coming straight from the opposite direction.",
        "template": "{n1} makes a U-turn and collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [1]
                },
                {
                    "name": "n2",
                    "actions": [4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "T-bone collision",
        "functional": "V1 is traveling straight through a four-way intersection when V2 turns right from a side road and collides with V1.",
        "template": "{n1} is collided by {n2} on the side, causing a collision, {others}, at {road}",
        "abstract": {
            "roads": [1],
            "norms": [
                {
                    "name": "n1",
                    "actions": [4, 5]
                },
                {
                    "name": "n2",
                    "actions": [7]
                }
            ],
            "agents": list(range(2, 5))
        }
    },
    {
        "type": "side-rear collision",
        "functional": "V1 is changing to the right lane and V2 collides into the rear-right side of V1.",
        "template": "{n1} gets hit on the rear-right side by {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [6]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": list(range(2, 5))
        }
    }
]


def generate_prompt(scenario):
    abstract = scenario["abstract"]
    road = random.choice(abstract["roads"])
    norms = abstract["norms"]

    agents = [0] + list(range(1, random.choice(abstract["agents"])))
    random.shuffle(agents[1:])

    prompt_str = scenario["template"]
    norm_strs = {}
    others_str = ""

    for i, id in enumerate(agents):
        agent = id + 1
        if i < len(norms):
            norm = norms[i]
            norm_strs[norm["name"]] = f"V{agent}"
            others_str += f"V{agent} {actions[random.choice(norm['actions'])]} and "
        else: others_str += f"V{agent} {actions[random.choice(roads[road]['actions'])]} and "

    prompt_str = prompt_str.format_map({
        **norm_strs,
        "others": "and ".join(others_str.split("and ")[:-1]).strip(),
        "road": roads[road]["name"]
    })

    return prompt_str


if __name__ == "__main__":
    print(generate_prompt(random.choice(scenarios)))
