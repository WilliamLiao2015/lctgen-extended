import random


roads = [
    "a two-way intersection",
    "a four-way intersection",
    "a T-intersection",
    "a roundabout"
]

actions = ["stop", "turn left", "change to left lane", "decelerate", "keep speed", "accelerate", "change to right lane", "turn right"]

prompts = [
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
    }
]


def generate_prompt(prompt):
    abstract = prompt["abstract"]
    road = random.choice(abstract["roads"])
    norms = abstract["norms"]

    agents = [0] + list(range(1, random.choice(abstract["agents"])))
    random.shuffle(agents[1:])

    prompt_str = prompt["template"]
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
    print(generate_prompt(random.choice(prompts)))
