import torch

def get_surface_hit_ts(rays: dict, surface_point, surface_normal, t_max=100000) -> torch.Tensor:
    """
    Get the t of intersection of rays with a surface.
    surface_point - vec3
    surface_normal - vec3
    """
    P0 = surface_point
    n = surface_normal
    d_array = rays['direction']
    O = rays['origin']
    divisor = torch.matmul(d_array, n)
    divisor[divisor == 0] = 1e-10
    t_array = torch.matmul(P0 - O, n) / divisor
    t_array[t_array < 1e-6] = torch.inf # Negatives or at the beginning
    t_array[t_array > t_max] = torch.inf
    return t_array

def get_surface_hit_ts_mask(hit_ts):
    return torch.abs(hit_ts) < torch.inf
