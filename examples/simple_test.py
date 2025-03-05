import numpy as np
from optics_raytracer.camera import SimpleCamera, FloatSize, IntegerSize
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Create camera
camera = SimpleCamera.build(
    camera_center=np.array([0, 0, 0], dtype=np.float32),
    focal_distance=1.0,
    viewport_size=FloatSize(2, 2),
    image_size=IntegerSize(400, 400),
    viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
    viewport_normal=np.array([0, 0, -1], dtype=np.float32)
)

# Create a lens
lens = Lens.build(
    center=np.array([0, 0, -2], dtype=np.float32),
    radius=1.0,
    normal=np.array([0, 0, -1], dtype=np.float32),
    focal_distance=1.0
)

# Create an image
image = InsertedImage(
    image_path="examples/image.png",
    width=4.0,
    height=4.0,
    middle_point=np.array([0, 0, -5], dtype=np.float32),
    normal=np.array([0, 0, -1], dtype=np.float32),
    u_vector=np.array([1, 0, 0], dtype=np.float32)
)

# Create ray tracing engine
engine = OpticsRayTracingEngine(
    camera=camera,
    objects=[image],
    lenses=[lens],
    ray_sampling_rate_for_3d_export=0.01
)

# Render the scene
engine.render(
    output_image_path="examples/output.png",
    output_3d_path="examples/scene.obj"
)

print("Rendering complete. Check examples/output.png for the result.")
