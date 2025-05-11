"""
Lens Comparison Experiment: Compare positive and negative lenses at different distances.

This experiment creates an animation showing how both positive (converging) and 
negative (diverging) lenses affect light rays as they move away from the camera.
The lenses are offset from each other to show the different effects simultaneously.

Output file:
- experiments/lens_comparison.gif: Animated GIF showing both lenses at increasing distances
"""

import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.gif_builder import GifBuilder
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# Configuration constants (all distances in decimeters)
TOTAL_FRAMES = 20
EYE_LENS_FOCAL_DISTANCE = 0.24
EYE_LENS_DISTANCE = 0.24
EYE_LENS_RADIUS = 0.01
IMAGE_DISTANCE = 50.0  # 5m
LENS_RADIUS = 4.0
POSITIVE_LENS_FOCAL_DISTANCE = 10.0   # Converging lens
NEGATIVE_LENS_FOCAL_DISTANCE = -10.0  # Diverging lens
LENS_DISTANCE_STEP = 2.0              # Distance increment per frame
POSITIVE_LENS_OFFSET = np.array([0, -5, 0], dtype=np.float32)  # Y offset for positive lens
NEGATIVE_LENS_OFFSET = np.array([5, 5, 0], dtype=np.float32)   # X,Y offset for negative lens

print(f"Starting lens comparison experiment ({TOTAL_FRAMES} frames)...")

# Create a GIF builder
gif_builder = GifBuilder()

# Process each frame
for i in range(TOTAL_FRAMES):
    lens_distance = (i + 1) * LENS_DISTANCE_STEP
    
    print(f"Processing frame {i+1}/{TOTAL_FRAMES}: Lenses at {lens_distance}dm")
    
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

    # Create positive lens (converging)
    positive_lens = Lens.build(
        center=np.array([0, 0, -lens_distance], dtype=np.float32) + POSITIVE_LENS_OFFSET,
        radius=LENS_RADIUS,
        normal=np.array([0, 0, -1], dtype=np.float32),
        focal_distance=POSITIVE_LENS_FOCAL_DISTANCE,
    )

    # Create negative lens (diverging)
    negative_lens = Lens.build(
        center=np.array([0, 0, -lens_distance], dtype=np.float32) + NEGATIVE_LENS_OFFSET,
        radius=LENS_RADIUS,
        normal=np.array([0, 0, -1], dtype=np.float32),
        focal_distance=NEGATIVE_LENS_FOCAL_DISTANCE,
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
        lenses=[positive_lens, negative_lens],
        ray_sampling_rate_for_3d_export=0.01,
    )

    # Render the scene
    image = engine.render()
    
    # Add frame to animation
    gif_builder.add_image(image)

# Save the completed animation
gif_builder.save("experiments/lens_comparison.gif")
print("Animation complete! Saved to experiments/lens_comparison.gif")
