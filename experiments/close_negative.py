import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize, SimpleCamera
from optics_raytracer.gif_builder import GifBuilder
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Setup parameters - eye lens focal distance in decimeters
lens_focal_distance = 0.24

print(f"Starting lens comparison experiment (frame {0+1}/10)...")
print(f"Using eye lens with focal distance: {lens_focal_distance} dm")

# Create eye camera at origin (0,0,0) simulating human eye
camera = EyeCamera.build(
    viewport_center=np.array([0, 0, 0], dtype=np.float32),
    lens_distance=0.24,  # 0.24dm lens distance
    lens_radius=.01,
    number_of_circles=2,
    rays_per_circle=5,
    viewport_size=FloatSize(.35, .35),
    image_size=IntegerSize(200, 200),  # Higher resolution for better detail
    viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
    viewport_normal=np.array([0, 0, -1], dtype=np.float32),
    lens_focal_distance=lens_focal_distance
)

# camera = SimpleCamera.build(
#     camera_center=np.array([0, 0, 0], dtype=np.float32),
#     focal_distance=0.24,  # 0.24dm lens distance
#     viewport_size=FloatSize(.35, .35),
#     image_size=IntegerSize(200, 200),  # Higher resolution for better detail
#     viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
#     viewport_normal=np.array([0, 0, -1], dtype=np.float32)
# )

print("Camera setup complete.")
print(f"Setting up test lenses at {(1)*4}dm distance...")

# Create two test lenses at varying distances (moving farther with each frame)
# First lens with positive focal distance (converging lens)
lens = Lens.build(
    center=np.array([0, 0, -((1) * 4)], dtype=np.float32),  # 2.5m away
    radius=4.0,
    normal=np.array([0, 0, -1], dtype=np.float32),
    focal_distance=-10.0  # 1m positive focal distance
)

print(f"Lenses created: positive lens (f=10dm) and negative lens (f=-10dm) at {(0+1)*4}dm")
print("Setting up test image at 50dm (5m) distance...")

# Create an image at 5m (50dm)
distant_image = InsertedImage(
    image_path="target.png",
    width=50.0,
    height=50.0,
    middle_point=np.array([0, 0, -50], dtype=np.float32),  # 5m away
    normal=np.array([0, 0, -1], dtype=np.float32),
    u_vector=np.array([1, 0, 0], dtype=np.float32)
)

print("Test image loaded successfully.")
print("Initializing ray tracing engine...")

# Create ray tracing engine
engine = OpticsRayTracingEngine(
    camera=camera,
    objects=[distant_image],
    lenses=[lens],
    ray_sampling_rate_for_3d_export=0.01
)

print("Ray tracing engine initialized with camera, lenses, and image.")
print("Starting rendering process...")

# Render the scene and save individual frame OBJ files
image = engine.render(
    output_3d_path="close_negative.obj",
    output_image_path="close_negative.png"
)
