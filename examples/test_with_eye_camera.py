import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Create eye camera
camera = EyeCamera.build(
    camera_center=np.array([0, 0, 0], dtype=np.float32),
    lens_distance=5.0,
    lens_radius=2.0,
    number_of_circles=2,
    rays_per_circle=5,
    viewport_size=FloatSize(10.0, 10.0),
    image_size=IntegerSize(120, 120),
    viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
    viewport_normal=np.array([0, 0, -1], dtype=np.float32),
    lens_focal_distance=5.0
)

# Create a lens
lens = Lens.build(
    center=np.array([0, 0, -10], dtype=np.float32),
    radius=2.0,
    normal=np.array([0, 0, 1], dtype=np.float32),
    focal_distance=15.0
)

# Create an image from image.png
image = InsertedImage(
    image_path="examples/image.png",
    width=10.0,
    height=10.0,
    middle_point=np.array([0, 0, -15], dtype=np.float32),
    normal=np.array([0, 0, -1], dtype=np.float32),
    u_vector=np.array([1, 0, 0], dtype=np.float32)
)

# Create ray tracing engine
engine = OpticsRayTracingEngine(
    camera=camera,
    objects=[image],
    lenses=[
        # lens
        ],
    ray_sampling_rate_for_3d_export=0.01
)

# Render the scene
engine.render(
    output_image_path="examples/output.png",
    output_3d_path="examples/microscope_scene.obj"
)
