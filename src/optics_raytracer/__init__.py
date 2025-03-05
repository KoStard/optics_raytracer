from .primitives import vector_dtype, color_dtype, point_dtype
from .ray import ray_dtype, get_ray_point_at_t, get_ray_points_array_at_t_array, build_rays
from .surface import surface_dtype, get_surface_hit_ts, get_surface_hit_ts_mask
from .rectangle import rectangle_dtype, Rectangle
from .circle import circle_dtype, Circle
from .lens import lens_dtype, Lens
from .camera import simple_camera_viewport_dtype, Camera, SimpleCamera, EyeCamera, eye_camera_viewport_dtype
from .cli import main
from .color_tracer import ColorTracer
from .colored_object import ColoredObject
from .engine import OpticsRayTracingEngine
from .export_3d import Exporter3D
from .gif_builder import GifBuilder
from .image_saver import ImageSaver
from .inserted_image import InsertedImage
from .pixelated_viewport import build_pixelated_viewport, pixelated_viewport_dtype, get_pixel_points
from .size import IntegerSize, FloatSize

__all__ = [
    'vector_dtype',
    'color_dtype', 
    'point_dtype',
    'ray_dtype',
    'get_ray_point_at_t',
    'get_ray_points_array_at_t_array',
    'build_rays',
    'surface_dtype',
    'get_surface_hit_ts',
    'get_surface_hit_ts_mask',
    'rectangle_dtype',
    'Rectangle',
    'circle_dtype',
    'Circle',
    'lens_dtype',
    'Lens',
    'simple_camera_viewport_dtype',
    'eye_camera_viewport_dtype',
    'Camera',
    'SimpleCamera',
    'EyeCamera',
    'main',
    'ColorTracer',
    'ColoredObject',
    'OpticsRayTracingEngine',
    'Exporter3D',
    'GifBuilder',
    'ImageSaver',
    'InsertedImage',
    'build_pixelated_viewport',
    'pixelated_viewport_dtype',
    'get_pixel_points',
    'IntegerSize',
    'FloatSize',
]
