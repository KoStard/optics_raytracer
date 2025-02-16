from .camera import Camera
from .image_save import ImageSaver
from .inserted_image import InsertedImage
from .lens import Lens
from .ray import Ray
from .size import IntegerSize
from .vec3 import Color3, Point3, Vec3
from PIL import Image
from .export_3d import Exporter3D
import random

class OpticsRayTracingEngine:
    def __init__(self, camera: Camera, hittables: list, image_size: IntegerSize):
        self.camera = camera
        self.hittables = hittables
        self.image_size = image_size
        self.image_saver = ImageSaver(image_size.width, image_size.height)
        self.exporter = Exporter3D()

    def trace_ray(self, ray: Ray, depth=0, max_depth=5):
        if depth > max_depth:
            return Color3(0,0,0)
        closest_t = float("inf")
        hit_obj = None
        for obj in self.hittables:
            t = obj.hit(ray)
            if t is not None and t < closest_t:
                closest_t = t
                hit_obj = obj
        if hit_obj is None:
            return Color3(0,0,0)
        hit_point = ray.at(closest_t)
        if random.random() < 0.05:
            self.exporter.add_point(hit_point)
            self.exporter.add_line(ray.origin, hit_point)
        if hasattr(hit_obj, "get_new_ray"):
            new_ray = hit_obj.get_new_ray(ray, hit_point)
            return self.trace_ray(new_ray, depth+1, max_depth)
        elif hasattr(hit_obj, "get_color"):
            return hit_obj.get_color(ray, hit_point)
        else:
            raise Exception("Hit object type not handled")

    def render(self, image_output_path: str, export_3d: bool = False, obj_output_path: str = None):
        for camera_image_row, camera_image_column, ray in self.camera.get_rays():
            print(f"\rScanlines remaining: {self.camera.viewport.pixel_rows - camera_image_row} ", end="", flush=True)
            color = self.trace_ray(ray)
            self.image_saver.add_pixel(color)

        if export_3d:
            if not obj_output_path:
                raise ValueError("obj_output_path must be specified when export_3d is True")
            for obj in self.hittables:
                if isinstance(obj, Lens):
                    self.exporter.add_circle(obj)
                elif isinstance(obj, InsertedImage):
                    self.exporter.add_rectangle(obj)
            if hasattr(self.camera, "viewport"):
                self.exporter.add_rectangle(self.camera.viewport)
            self.exporter.save_to_obj(obj_output_path)

        self.image_saver.save(image_output_path)

if __name__ == "__main__":
    # Example usage
    camera_image_size = IntegerSize.from_width_and_aspect_ratio(400, 16/9)
    camera = Camera(Point3(0, 0, 0), 
                    1,
                    camera_image_size.float_scale_to_width(2),
                    camera_image_size,
                    Vec3(1, 0, 0),  # right
                    Vec3(0, 0, -1)   # the normal of the viewport away from camera - this way the y is down
                    )

    image_path = "image.png"
    image = Image.open(image_path)
    image_size = IntegerSize(image.width, image.height)
    image_viewport_width = 4
    inserted_image = InsertedImage(
        Point3(-2, 1, -4),
        image_viewport_width,
        image_size.float_scale_to_width(image_viewport_width).height,
        Vec3(1, 0, 0),
        Vec3(0, 0, -1),
        image
    )

    lens_1 = Lens(Point3(0, 0, -2), 1, Vec3(0, 0, -1), -1)
    lens_2 = Lens(Point3(0, 0, -3), 1, Vec3(0, 0, -1), 1)

    hittables = [lens_1, lens_2, inserted_image]

    engine = OpticsRayTracingEngine(camera, hittables, camera_image_size)
    engine.render('image.ppm', export_3d=True, obj_output_path='export.obj')
