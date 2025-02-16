from .pixelated_viewport import PixelatedViewport
from .ray import Ray
from .size import IntegerSize
from .vec3 import Point3, Vec3


class Camera:
    def __init__(self, camera_center: Point3, focal_distance: float, viewport_size: IntegerSize, image_size: IntegerSize, viewport_u_vector: Vec3, viewport_normal: Vec3):
        # viewport_normal is the continuation of the camera to viewport center vector
        viewport_normal = viewport_normal.unit_vector
        viewport_center = camera_center + focal_distance * viewport_normal
        viewport_v_vector = viewport_normal.cross(viewport_u_vector)
        viewport_left_top = viewport_center - viewport_u_vector * viewport_size.width / 2 - viewport_v_vector * viewport_size.height / 2
        self.viewport = PixelatedViewport(
            viewport_left_top,
            viewport_size.width,
            viewport_size.height,
            viewport_u_vector,
            viewport_normal,
            image_size.width,
            image_size.height
        )
        self.camera_center = camera_center
    
    def get_rays(self):
        for row in range(self.viewport.pixel_rows):
            for column in range(self.viewport.pixel_columns):
                pixel_point = self.viewport.get_pixel_point(column, row)
                yield row, column, Ray(self.camera_center, pixel_point - self.camera_center)
