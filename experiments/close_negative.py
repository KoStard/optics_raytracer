"""
Negative Lens Experiment: Visualize how a negative lens affects light rays.

This experiment places a negative lens at a fixed distance of 4dm from the camera
and renders the scene with a target image at 50dm (5m) distance. The simulation 
demonstrates how a negative lens causes light rays to diverge.

Output files:
- experiments/close_negative.png: Rendered image
- experiments/close_negative.obj/.mtl: 3D scene visualization
"""

import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Configuration constants (all distances in decimeters)
EYE_LENS_FOCAL_DISTANCE = 0.24
EYE_LENS_DISTANCE = 0.24
EYE_LENS_RADIUS = 0.01
IMAGE_DISTANCE = 50.0  # 5m 
LENS_DISTANCE = 4.0    # 4dm
LENS_RADIUS = 4.0
LENS_FOCAL_DISTANCE = -10.0  # Negative focal distance

print("Starting negative lens experiment...")

# Create eye camera at origin (0,0,0) simulating human eye
camera = EyeCamera.build(
    viewport_center=np.array([0, 0, 0], dtype=np.float32),
    lens_distance=EYE_LENS_DISTANCE,
    lens_radius=EYE_LENS_RADIUS,
    number_of_circles=2,
    rays_per_circle=5,
    viewport_size=FloatSize(0.35, 0.35),
    image_size=IntegerSize(200, 200),
    viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
    viewport_normal=np.array([0, 0, -1], dtype=np.float32),
    lens_focal_distance=EYE_LENS_FOCAL_DISTANCE,
)

# Create a negative lens
lens = Lens.build(
    center=np.array([0, 0, -LENS_DISTANCE], dtype=np.float32),
    radius=LENS_RADIUS,
    normal=np.array([0, 0, -1], dtype=np.float32),
    focal_distance=LENS_FOCAL_DISTANCE,
)

# Create a target image
distant_image = InsertedImage(
    image_path="experiments/assets/target.png",
    width=50.0,
    height=50.0,
    middle_point=np.array([0, 0, -IMAGE_DISTANCE], dtype=np.float32),
    normal=np.array([0, 0, -1], dtype=np.float32),
    u_vector=np.array([1, 0, 0], dtype=np.float32),
)

print(f"Setup complete: Eye lens (f={EYE_LENS_FOCAL_DISTANCE}dm), " 
      f"Negative lens (f={LENS_FOCAL_DISTANCE}dm) at {LENS_DISTANCE}dm, "
      f"Target image at {IMAGE_DISTANCE}dm")

# Create ray tracing engine and render
engine = OpticsRayTracingEngine(
    camera=camera,
    objects=[distant_image],
    lenses=[lens],
    ray_sampling_rate_for_3d_export=0.01,
)

print("Rendering scene...")
image = engine.render(
    output_3d_path="experiments/close_negative.obj",
    output_mtl_path="experiments/close_negative.mtl",
    output_image_path="experiments/close_negative.png"
)
print("Rendering complete! Output saved to experiments/close_negative.png")
