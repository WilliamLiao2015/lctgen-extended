import random


roads = [
    "a two-way intersection",
    "a four-way intersection",
    "a T-intersection",
    "a roundabout",
    "freeway"
]

actions = ["stop", "turn left", "change to left lane", "decelerate", "keep speed", "accelerate", "change to right lane", "turn right"]

scenarios = [
    {
        "type": "rear-end collision",
        "functional": "V1 goes straight and collides with V2 while V2 turns left",
        "template": "{n1} collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
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
            "agents": range(2, 5)
        }
    },
    {
        "type": "turn left",
        "functional": "V1 turns left at an intersection.",
        "template": "{n1}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
            "norms": [
                {
                    "name": "n1",
                    "actions": [1]
                }
            ],
            "agents": range(1, 5)
        }
    }, # for simplicity, right turn is temporarily ignored
    {
        "type": "change to left lane",
        "functional": "V1 changes to left lane.",
        "template": "{n1}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2, 4],
            "norms": [
                {
                    "name": "n1",
                    "actions": [2]
                }
            ],
            "agents": range(1, 5)
        }
    }, # for simplicity, changing to right lane is temprarily ignored
    {
        "type": "turning collision",
        "functional": "V1 turns right and bumps into V2.",
        "template": "{n1} bumps into {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
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
            "agents": range(2, 5)
        }
    },
    {
        "type": "head-side collision",
        "functional": "V1 is travelling straight to the south in the intersection when V2 collides it straight from the east.",
        "template": "{n1} bumps into {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2],
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
            "agents": range(2, 5)
        }
    },
    {
        "type": "side-side collision",
        "functional": "V1 collides with V2 while V1 changes to left lane",
        "template": "{n1} collides with {n2}, {others}, at {road}",
        "abstract": {
            "roads": [0, 1, 2, 4],
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
            "agents": range(2, 5)
        }
    },
    { # assumption: left-hand driving countries (TW, US, etc.)
        "type": "head-head collision",
        "functional": "V1 drives to the opposite lane and crashes V2 while V2 goes straight",
        "template": "{n1} drives to the opposite lane and crashes {n2}, {others}, on {road}",
        "abstract": {
            "roads": [0, 1, 2, 4],
            "norms": [
                {
                    "name": "n1",
                    "actions": [1, 2]
                },
                {
                    "name": "n2",
                    "actions": [3, 4, 5]
                }
            ],
            "agents": range(2, 5)
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
        else: others_str += f"V{agent} {actions[random.choice(range(8))]} and "

    prompt_str = prompt_str.format_map({
        **norm_strs,
        "others": others_str.strip("and "),
        "road": roads[road]
    })

    return prompt_str


if __name__ == "__main__":
    print(generate_prompt(random.choice(scenarios)))
