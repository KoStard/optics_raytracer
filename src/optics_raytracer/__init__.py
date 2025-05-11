from optics_raytracer.core.primitives import vector_dtype, color_dtype, point_dtype
from optics_raytracer.utils.group_namer import GroupNamer
from optics_raytracer.core.ray import (
    ray_dtype,
    get_ray_point_at_t,
    get_ray_points_array_at_t_array,
    build_rays,
)
from optics_raytracer.core.surface import surface_dtype, get_surface_hit_ts, get_surface_hit_ts_mask
from optics_raytracer.geometry.rectangle import rectangle_dtype, Rectangle
from optics_raytracer.geometry.circle import circle_dtype, Circle
from optics_raytracer.optics.lens import lens_dtype, Lens
from optics_raytracer.camera.camera import (
    simple_camera_viewport_dtype,
    Camera,
    SimpleCamera,
    EyeCamera,
    eye_camera_viewport_dtype,
)
from optics_raytracer.cli import main, parse_config
from optics_raytracer.rendering.color_tracer import ColorTracer
from optics_raytracer.optics.colored_object import ColoredObject
from optics_raytracer.rendering.engine import OpticsRayTracingEngine
from optics_raytracer.rendering.export_3d import Exporter3D
from optics_raytracer.rendering.gif_builder import GifBuilder
from optics_raytracer.rendering.image_saver import ImageSaver
from optics_raytracer.objects.inserted_image import InsertedImage
from optics_raytracer.camera.pixelated_viewport import (
    build_pixelated_viewport,
    pixelated_viewport_dtype,
    get_pixel_points,
)
from optics_raytracer.utils.size import IntegerSize, FloatSize

__all__ = [
    "vector_dtype",
    "color_dtype",
    "point_dtype",
    "ray_dtype",
    "get_ray_point_at_t",
    "get_ray_points_array_at_t_array",
    "build_rays",
    "surface_dtype",
    "get_surface_hit_ts",
    "get_surface_hit_ts_mask",
    "rectangle_dtype",
    "Rectangle",
    "circle_dtype",
    "Circle",
    "lens_dtype",
    "Lens",
    "simple_camera_viewport_dtype",
    "eye_camera_viewport_dtype",
    "Camera",
    "SimpleCamera",
    "EyeCamera",
    "main",
    "parse_config",
    "ColorTracer",
    "ColoredObject",
    "OpticsRayTracingEngine",
    "Exporter3D",
    "GifBuilder",
    "ImageSaver",
    "InsertedImage",
    "build_pixelated_viewport",
    "pixelated_viewport_dtype",
    "get_pixel_points",
    "IntegerSize",
    "FloatSize",
    "GroupNamer",
]
