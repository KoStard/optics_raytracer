"""
Moving Lens Experiment: Visualize the effect of a negative lens at different distances.

This experiment creates an animation showing how a negative lens affects light rays
as it moves away from the camera. The lens starts at 4dm and moves to 40dm in 10 frames,
with each frame showing the lens at an increasing distance.

Output file:
- experiments/moving_lens.gif: Animated GIF of all frames
"""

import os
import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.gif_builder import GifBuilder
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Configuration constants (all distances in decimeters)
TOTAL_FRAMES = 10
EYE_LENS_FOCAL_DISTANCE = 0.24
EYE_LENS_DISTANCE = 0.24
EYE_LENS_RADIUS = 0.01
IMAGE_DISTANCE = 50.0  # 5m
LENS_RADIUS = 4.0
LENS_FOCAL_DISTANCE = -10.0  # Negative focal distance
LENS_DISTANCE_STEP = 4.0     # Distance increment per frame
GIF_FRAME_DURATION = 500     # Milliseconds per frame

# Create directory for frame files (if needed)
frames_dir = "experiments/moving_lens_frames"
os.makedirs(frames_dir, exist_ok=True)

print(f"Starting moving lens experiment ({TOTAL_FRAMES} frames)...")

# Create a GIF builder
gif_builder = GifBuilder(duration=GIF_FRAME_DURATION)

# Process each frame
for i in range(TOTAL_FRAMES):
    lens_distance = (i + 1) * LENS_DISTANCE_STEP
    
    print(f"Processing frame {i+1}/{TOTAL_FRAMES}: Lens at {lens_distance}dm")
    
    # Create eye camera
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

    # Create negative lens at current distance
    lens = Lens.build(
        center=np.array([0, 0, -lens_distance], dtype=np.float32),
        radius=LENS_RADIUS,
        normal=np.array([0, 0, -1], dtype=np.float32),
        focal_distance=LENS_FOCAL_DISTANCE,
    )

    # Create target image
    distant_image = InsertedImage(
        image_path="experiments/assets/target.png",
        width=50.0,
        height=50.0,
        middle_point=np.array([0, 0, -IMAGE_DISTANCE], dtype=np.float32),
        normal=np.array([0, 0, -1], dtype=np.float32),
        u_vector=np.array([1, 0, 0], dtype=np.float32),
    )

    # Create ray tracing engine and render
    engine = OpticsRayTracingEngine(
        camera=camera,
        objects=[distant_image],
        lenses=[lens],
        ray_sampling_rate_for_3d_export=0.01,
    )

    # Uncomment to save individual OBJ files:
    # output_3d_path=f"{frames_dir}/frame_{i+1:02d}.obj"
    # output_mtl_path=f"{frames_dir}/frame_{i+1:02d}.mtl"
    image = engine.render()
    
    # Add frame to animation
    gif_builder.add_image(image)

# Save the completed animation
gif_builder.save("experiments/moving_lens.gif")
print("Animation complete! Saved to experiments/moving_lens.gif")
