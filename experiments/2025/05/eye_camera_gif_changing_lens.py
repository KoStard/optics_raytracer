"""
Experiment: Eye camera with changing lens focal distance

This experiment shows an eye camera looking at an image through a lens.
The lens focal distance changes from negative to positive, showing the effect 
on the image (from concave to convex lens).
"""

import numpy as np
from pathlib import Path
from optics_raytracer import (
    EyeCamera, Lens, InsertedImage, OpticsRayTracingEngine,
    IntegerSize, FloatSize, GifBuilder
)
from PIL import Image

# Define parameters
NUM_FRAMES = 30
NUM_3D_EXPORTS = 5  # Number of frames to export as 3D models
OUTPUT_DIR = Path("experiments/2025/05/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create GIF builder
gif_builder = GifBuilder(optimize=True, duration=100)

# Define focal distance range (from negative to positive)
min_focal_distance = -2.0
max_focal_distance = 2.0
# Skip exact zero to avoid division by zero issues
focal_distances = np.linspace(min_focal_distance, max_focal_distance, NUM_FRAMES)
focal_distances = np.where(np.abs(focal_distances) < 0.1, 
                          np.sign(focal_distances) * 0.1, 
                          focal_distances)

# Setup scene components that don't change
image_path = "examples/assets/image.png"
image_size = IntegerSize(400, 400)

# Create inserted image (target)
image = InsertedImage(
    image_path=image_path,
    width=16.0,
    height=16.0,
    middle_point=np.array([0, 0, -10], dtype=np.float32),
    normal=np.array([0, 0, 1], dtype=np.float32),
    u_vector=np.array([1, 0, 0], dtype=np.float32)
)

for i, focal_distance in enumerate(focal_distances):
    print(f"Processing frame {i+1}/{NUM_FRAMES}: focal distance = {focal_distance:.2f}")
    
    # Create eye camera
    camera = EyeCamera.build(
        viewport_center=np.array([0, 0, 0], dtype=np.float32),
        lens_distance=0.24,
        lens_radius=0.5,
        number_of_circles=2,
        rays_per_circle=3,
        viewport_size=FloatSize(0.5, 0.5),
        image_size=image_size,
        viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
        viewport_normal=np.array([0, 0, -1], dtype=np.float32),
        lens_focal_distance=0.24  # Fixed focal distance for the eye's lens
    )
    
    # Create lens with changing focal distance
    lens = Lens.build(
        center=np.array([0, 0, -5], dtype=np.float32),
        radius=4,
        normal=np.array([0, 0, -1], dtype=np.float32),
        focal_distance=focal_distance  # This changes each frame
    )
    
    # Create ray tracing engine
    engine = OpticsRayTracingEngine(
        camera=camera,
        objects=[image],
        lenses=[lens],
        ray_sampling_rate_for_3d_export=0.005,  # Lower value for fewer rays in visualization
        compare_with_without_lenses=False
    )
    
    # Output paths
    frame_path = OUTPUT_DIR / f"eye_camera_changing_lens_frame_{i:03d}.png"
    
    # Determine if we should export 3D for this frame
    export_3d = False
    if NUM_3D_EXPORTS > 0:
        # Calculate which frames to export (equally distributed)
        export_indices = np.linspace(0, NUM_FRAMES-1, NUM_3D_EXPORTS, dtype=int)
        if i in export_indices:
            export_3d = True
    
    # Render the scene
    output_3d_path = None
    output_mtl_path = None
    
    if export_3d:
        output_3d_path = str(OUTPUT_DIR / f"eye_camera_changing_lens_3d_{i:03d}.obj")
        output_mtl_path = str(OUTPUT_DIR / f"eye_camera_changing_lens_3d_{i:03d}.mtl")
        print(f"  Exporting 3D model for frame {i}")
    
    result = engine.render(
        output_image_path=str(frame_path),
        output_3d_path=output_3d_path,
        output_mtl_path=output_mtl_path
    )
    
    # Add the rendered image to our GIF
    gif_builder.add_image(result)

# Save the final GIF
gif_path = "experiments/2025/05/eye_camera_changing_lens.gif"
gif_builder.save(gif_path)

print(f"GIF saved to {gif_path}")
