from .overlapped_area_rate import evaluate_overlapped_area_rate
from .car_collision_rate import evaluate_car_collision_rate
from .road_collision_rate import evaluate_road_collision_rate
from .minimum_speed_rate import evaluate_minimum_speed_rate

from imports.lctgen import transform_traj_output_to_waymo_agent

metrics = {
    'overlapped-area-rate': evaluate_overlapped_area_rate,
    'car-collision-rate': evaluate_car_collision_rate,
    'road-collision-rate': evaluate_road_collision_rate,
    'minimum-speed-rate': evaluate_minimum_speed_rate
}

def wrapper(metric):
    def evaluate(model_output):
        agents = transform_traj_output_to_waymo_agent(model_output["text_scene_output"][0])
        return [metric(model_output, agents, t) for t in range(50)]
    return evaluate
