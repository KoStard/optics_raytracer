import numpy as np
from pathlib import Path
from optics_raytracer import (
    EyeCamera, FloatSize, IntegerSize, InsertedImage, OpticsRayTracingEngine
)

# Experiment configuration
FOCUS_DISTANCE = 5.0  # Object distance at focus in decimeters
IMAGE_POSITIONS = [2.5, 5.0, 10.0]  # Positions of the three images in decimeters
IMAGE_PATH = "examples/assets/apple.png"
OUTPUT_DIR = Path("experiments/2025/05/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Eye camera parameters
EYE_LENS_DISTANCE = 0.24  # Distance from lens to viewport in decimeters
EYE_LENS_RADIUS = 0.05
RAYS_PER_CIRCLE = 3
NUMBER_OF_CIRCLES = 2
IMAGE_SIZE = IntegerSize(400, 400)

# Create eye camera with focus at specified distance
camera = EyeCamera.build_from_focus_distance(
    viewport_center=np.array([0, 0, 0], dtype=np.float32),
    lens_distance=EYE_LENS_DISTANCE,
    lens_radius=EYE_LENS_RADIUS,
    object_distance=FOCUS_DISTANCE,
    number_of_circles=NUMBER_OF_CIRCLES,
    rays_per_circle=RAYS_PER_CIRCLE,
    viewport_size=FloatSize(0.35, 0.35),
    image_size=IMAGE_SIZE,
    viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
    viewport_normal=np.array([0, 0, -1], dtype=np.float32),
)

# Create images at different distances
images = []
image_width = 2.0  # Base image width
HORIZONTAL_OFFSET = [
    -1.5,  # Left image
    0,     # Middle image
    3    # Right image
]

for i, position in enumerate(IMAGE_POSITIONS):
    # Position images side by side with horizontal offset
    horizontal_offset = HORIZONTAL_OFFSET[i]
    
    # Create the image
    images.append(
        InsertedImage(
            image_path=IMAGE_PATH,
            width=image_width * (i + 1),
            height=image_width * (i + 1),
            # Position with offsets
            middle_point=np.array([horizontal_offset, 0, -position], dtype=np.float32),
            # Normal pointing back toward camera so we can see from behind
            normal=np.array([0, 0, -1], dtype=np.float32),
            u_vector=np.array([1, 0, 0], dtype=np.float32),
        )
    )

# Create and run the ray tracing engine
engine = OpticsRayTracingEngine(
    camera=camera,
    objects=images,
    lenses=[],  # No additional lenses beyond the eye camera's lens
    ray_sampling_rate_for_3d_export=0.05,
    compare_with_without_lenses=False,  # Compare with and without lens effects
)

# Render the scene
engine.render(
    output_image_path=str(OUTPUT_DIR / "focus_distance_test.png"),
    output_3d_path=str(OUTPUT_DIR / "focus_distance_test.obj"),
    output_mtl_path=str(OUTPUT_DIR / "focus_distance_test.mtl"),
)

print(f"Experiment complete. Results saved to {OUTPUT_DIR}")
