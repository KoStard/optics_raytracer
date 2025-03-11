import torch

def get_ray_point_at_t(ray, t):
    return ray['origin'] + t * ray['direction']

def get_ray_points_array_at_t_array(rays, t_array):
    return rays['origin'] + t_array[:, torch.newaxis] * rays['direction']

def build_rays(origins, directions):
    if origins.shape != directions.shape:
        print(origins.shape)
        print(directions.shape)
        raise ValueError("Origins and directions arrays must have the same shape.")

    rays = {}

    rays['origin'] = origins
    rays['direction'] = directions

    return rays

def apply_mask_on_rays(rays, mask):
    return {key: value[mask] for key, value in rays.items()}
