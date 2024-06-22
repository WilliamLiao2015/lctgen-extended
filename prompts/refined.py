import json

import numpy as np


metric_str_template = '''
Evaluating method: evaluate_overlapped_area_rate
Overlapped area rate: {oar:.2f}%

Evaluating method: evaluate_road_collision_rate
Road collision rate: {rcr:.2f}%

Evaluating method: evaluate_car_collision_rate
Car collision rate: {ccr:.2f}%

Evaluating method: evaluate_minimum_speed_rate
Minimum speed rate: {msr:.2f}%
'''


refined_prompt_template = '''
You are a highly skilled assistant specializing in refining and improving structured representations. Given the following initial structured data and additional information, your task is to refine the structured output, ensuring accuracy, completeness, and clarity. Follow these steps:

1. Review the Initial Structured Data: Examine the provided structured data to understand its current format and content.
2. Incorporate Additional Information: Integrate the additional information provided into the structured data, making sure to fill in any gaps, correct any inaccuracies, and enhance the overall quality of the data.
3. Ensure Consistency and Clarity: Make sure the final output is consistent in format and easy to understand. Use clear and concise language and structure the data logically.
4. Rethink and Modify: Assess the correctness of the position, distance, direction, and speed of the agent vectors. If the attributes is not reasonable, modify it based on your judgement.
5. Output the Refined Structured Data: Present the improved structured data clearly, maintaining a professional and polished format. Do not output the initial structured data.

## Additional Information

- You should only modify existing attributes in the Actor Vector, especially the first four attributes in the Actor Vector (pos, distance, direction, speed).
- The number of the agents should remain the same as the initial structured data.

### Query

The initial query that describes the actions of the vehicles in the scenario.

### Actor Vector

A list of vectors describing the attributes of each of the vehicles in the scenario, you only output the values without any text:

```
Meaning of the Actor vector attribute:
- dim 0: 'pos': [-1,3] - whether the vehicle is in the four quadrant of ego vechile in the order of [0 - 'front left', 1 - 'back left', 2- 'back right', 3 - 'front right']. -1 if the vehicle is the ego vehicle.
- dim 1: 'distance': [0,3] - the distance range index of the vehicle towards the ego vehicle; range is from 0 to 72 meters with 20 meters interval. 0 if the vehicle is the ego vehicle. For example, if distance value is 15 meters, then the distance range index is 0.
- dim 2: 'direction': [0,3] - the direction of the vehicle relative to the ego vehicle, in the order of [0- 'parallel_same', 1-'parallel_opposite', 2-'perpendicular_up', 3-'perpendicular_down']. 0 if the vehicle is the ego vehicle.
- dim 3: 'speed': [0,8] - the speed range index of the vehicle; range is from 0 to 20 m/s with 2.5 m/s interval. For example, 20m/s is in range 8, therefore the speed value is 8.
- dim 4-7: 'action': [0,7] - 4-dim, generate actions into the future 4 second with each two actions have a time interval of 1s (4 actions in total), the action ids are [0 - 'stop', 1 - 'turn left', 2 - 'left lane change', 3- 'decelerate', 4- 'keep_speed', 5-'accelerate',  6-'right lane change', 7-'turn right'].
```

### Metrics:

```
- Critical Area Rate:
    The critical area rate (CAR) is inspired by the conflict area mentioned in the literature above, indicating the likelihood of a collision occurring in a traffic scenario after a specific point in time.
    Due to the significant inertia of vehicles, sharp turns are difficult. Therefore, we define the critical area of a vehicle at a specific point in time as a sector with a radius equal to the speed, extending 30 degrees to either side of the current direction of travel.
    In summary, $CAR$ is calculated by dividing the total overlapped critical area by the total area of all overlapping critical areas. Since our goal is to generate critical scenario, a low CAR is undesirable.
- Road Collision Rate:
    The road collision rate (RCR) is determined by calculating the number of vehicles whose bounding boxes collide with the road boundaries, divided by the total number of vehicles. It indicates the degree of irrationality in a traffic scenario at a specific point in time. Under normal circumstances, no vehicle's bounding box should collide with the road boundaries.
- Car Collision Rate:
    The car collision rate (CCR) is calculated by dividing the number of all crashed vehicles by the total number of vehicles. It indicates the level of danger in a traffic scenario at a specific point in time. In a traffic scenario considered safe, the $CCR$ is expected to be $0$, as no two vehicles should collide, but our goal is to generate critical traffic scenario, a CCR of $0$ is not desirable, indicating a bad structured output.
- Minimum Speed Rate:
    The minimum speed rate (MSR) is calculated by dividing the minimum speed among all vehicles by the average speed of all vehicles. It indicates the fluidity of a traffic scenario at a specific point in time and can roughly serve as an indicator of the danger level.
```

## Explanation

Initial Structured Data: This is the starting point. It represents the initial state of the structured data.

Refined Structured Data: This is where the assistant outputs the improved version of the structured data, incorporating all the additional information and ensuring clarity and accuracy.

## How It Came to Be

- Clarity and Specificity: The prompt clearly defines the task and the steps the assistant should follow, minimizing ambiguity.
- Contextual Information: By providing both the initial data and additional information, the assistant has all the necessary context to refine the output effectively.
- Structured Format: Using a structured format (like tables) helps in organizing the data logically and making the task clear for the assistant.
- Example: Providing an example ensures that the assistant understands the expected format and style of the refined output.

## Example Prompt

### Initial Structured Data

```
Query: V1 turn left, V2 goes straight and accelerate, V3 slow down, at a two way intersection

---

Actor Vector:
- 'V1': [-1, 0, 0, 2, 1, 1, 1, 1]
- 'V2': [0, 0, 0, 4, 5, 5, 5, 5]
- 'V3': [0, 0, 0, 2, 3, 3, 3, 3]
Map Vector:
- 'Map': [1, 1, 1, 1, 0, 1]

---

Evaluating method: evaluate_overlapped_area_rate
Overlapped area rate: 0.10%

Evaluating method: evaluate_road_collision_rate
Road collision rate: 12.00%

Evaluating method: evaluate_car_collision_rate
Car collision rate: 0.00%

Evaluating method: evaluate_minimum_speed_rate
Minimum speed rate: 45.22%
```

### Refined Structured Data

```
Actor Vector:
- 'V1': [-1, 0, 0, 2, 1, 1, 1, 1]
- 'V2': [3, 1, 2, 4, 5, 5, 5, 5]
- 'V3': [0, 0, 0, 2, 3, 3, 3, 3]
Map Vector:
- 'Map': [1, 1, 1, 1, 0, 1]
```

## Prompt

### Initial Structured Data

```
Query: {query}

---

{llm_result}

---

{metric_str}
```

### Refined Structured Data

```
```
'''


def generate_refined_prompt(query: str, llm_result: str, state_str: str):
    state_str_js = json.loads(state_str)
    metrics_eval = []

    for k in state_str_js['results'].keys():
        metrics_eval.append(np.mean(state_str_js['results'][k]))

    oar, rcr, ccr, msr = metrics_eval

    refined_prompt = refined_prompt_template.format(query=query, llm_result=llm_result, metric_str=metric_str_template.format(oar=oar, rcr=rcr, ccr=ccr, msr=msr))

    print(refined_prompt)

    return refined_prompt
