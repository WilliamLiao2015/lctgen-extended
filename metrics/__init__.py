from imports.lctgen import transform_traj_output_to_waymo_agent

from .overlapped_area_rate import evaluate_overlapped_area_rate
from .car_collision_rate import evaluate_car_collision_rate
from .road_collision_rate import evaluate_road_collision_rate
from .minimum_speed_rate import evaluate_minimum_speed_rate

metrics = {
    "overlapped-area-rate": [evaluate_overlapped_area_rate, lambda before, after: before - after],
    "car-collision-rate": [evaluate_car_collision_rate, lambda before, after: before - after],
    "road-collision-rate": [evaluate_road_collision_rate, lambda before, after: after - before],
    "minimum-speed-rate": [evaluate_minimum_speed_rate, lambda before, after: before - after]
}

def wrapper(metric):
    def evaluate(model_output, original=False):
        agents = transform_traj_output_to_waymo_agent(model_output[f"{'original_' if original else ''}text_scene_output"][0])
        end_frame = [t for t in range(50) if evaluate_car_collision_rate(model_output, agents, t) > 0][0]
        return [metric(model_output, agents, t) for t in range(end_frame + 1)]
    return evaluate
