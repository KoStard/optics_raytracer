# Optics Raytracer

A 3D optics raytracer for simulating thin lenses and image projection, with OBJ export capabilities.

## Features

- Thin lens simulation with focal distances
- Image projection through lenses
- Ray visualization in 3D space
- 3D scene export to OBJ format
- Clear group naming in OBJ files
- Multiple configuration methods (CLI, Python, JSON)

![Optics Simulation](https://github.com/user-attachments/assets/ea337d37-45da-4bc2-a82c-38d84c8d583a)

3D Examples:
- [Demo with Eye-like camera with focal distance](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/eye_like_camera/test_with_eye.obj,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/eye_like_camera/test_with_eye.mtl)
- [Simple Telescope](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/telescope/telescope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/telescope/telescope_scene.obj)
- [Simple Microscope](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/microscope/microscope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/microscope/microscope_scene.obj)


## Installation

Install using pip or uv:

```bash
uv add --upgrade git+https://github.com/KoStard/optics_raytracer
# or
pip install git+https://github.com/KoStard/optics_raytracer

# or, if using from CLI
uv tool install git+https://github.com/KoStard/optics_raytracer
```

## Usage

### 1. CLI Configuration (JSON)

Create a config.json file:
```python
{
    "camera": {
        "center": [x, y, z],          # Camera position in 3D space
        "focal_distance": 1.0,        # Distance from camera to viewport
        "viewport_width": 2.0,        # Width of viewport in world units
        "image_size": [w, h],         # Output image resolution in pixels
        "u_vector": [x, y, z],        # Right direction vector (typically [1,0,0])
        "viewport_normal": [x, y, z]  # Direction camera is pointing (away from camera)
    },
    "objects": [
        {
            "type": "lens",           # Type of object
            "center": [x, y, z],      # Lens center position
            "radius": 1.0,            # Lens radius
            "normal": [x, y, z],      # Lens orientation (normal vector)
            "focal_distance": -1.0    # Focal length (positive for convex, negative for concave)
        },
        {
            "type": "lens",           # Second lens
            "center": [x, y, z],
            "radius": 1.0,
            "normal": [x, y, z],
            "focal_distance": 1.0
        },
        {
            "type": "image",          # Type of object
            "image_path": "examples/image.png", # Path to source image file
            "width": 4.0,             # Physical width of image in world units
            "center": [x, y, z],      # Center position of image
            "normal": [x, y, z],      # Image plane orientation (normal vector)
            "u_vector": [x, y, z]     # Right direction vector of image plane
        }
    ],
    "output": {
        "image_path": "output.png",   # Path to save rendered image
        "obj_path": "scene.obj"       # Path to save 3D scene (optional)
    },
    "ray_sampling_rate": 0.01,        # Rate for sampling rays in 3D export (optional)
    "compare_with_without_lenses": true # Generate side-by-side comparison with/without lenses (optional)
}
```

### Configuration Attributes Explained

#### Camera Settings
- **center**: The 3D position of the camera in world coordinates (x,y,z)
- **focal_distance**: Distance from camera to the viewport plane
- **viewport_width**: Width of viewport in world units (height calculated based on aspect ratio)
- **image_size**: Resolution of output image in pixels [width, height]
- **u_vector**: Right direction vector of the camera (typically [1,0,0])
- **viewport_normal**: Direction the camera is pointing (normal vector away from camera)

#### Object Settings
- **type**: Type of object ("lens" or "image")
- For lenses:
  - **center**: 3D position of lens center
  - **radius**: Physical radius of lens
  - **normal**: Orientation of lens (normal vector)
  - **focal_distance**: Focal length (positive for convex, negative for concave lenses)
- For images:
  - **image_path**: Path to source image file
  - **width**: Physical width of image in world units
  - **center**: Center position of image in 3D space
  - **normal**: Orientation of image plane (normal vector)
  - **u_vector**: Right direction vector of image plane

#### Output Settings
- **image_path**: Path to save rendered output image
- **obj_path**: Path to save 3D scene file (optional)

#### Additional Settings
- **ray_sampling_rate**: Rate for sampling rays in 3D export (optional, default value used if not specified)
- **compare_with_without_lenses**: If true, renders the scene twice (with and without lenses) and combines the results into a single side-by-side comparison image (optional, default is false)

#### Examples

Example config files are available in the `examples/` directory. Run them with:

```bash
# Run telescope example
optics-raytracer examples/telescope.json

# Run microscope example
optics-raytracer examples/microscope.json
```

### 2. Python Configuration

```python
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
    ray_sampling_rate_for_3d_export=0.01,
    compare_with_without_lenses=True  # Generate side-by-side comparison
)

# Render the scene
engine.render(
    output_image_path="examples/output.png",
    output_3d_path="examples/scene.obj"
)

print("Rendering complete. Check examples/output.png for the result.")
```

### 3. Dictionary Configuration from Python

```python
from optics_raytracer.cli import parse_config

# Define the scene using a dictionary (similar to JSON structure
config = {
    "camera": {
        "center": [0, 0, 0],
        "focal_distance": 1.0,
        "viewport_width": 2.0,
        "image_size": [400, 400],
        "u_vector": [1, 0, 0],
        "viewport_normal": [0, 0, -1]
    },
    "objects": [
        {
            "type": "lens",
            "center": [0, 0, -2],
            "radius": 1.0,
            "normal": [0, 0, -1],
            "focal_distance": 1.0
        },
        {
            "type": "image",
            "image_path": "examples/image.png",
            "width": 4.0,
            "center": [0, 0, -5],
            "normal": [0, 0, -1],
            "u_vector": [1, 0, 0]
        }
    ],
    "output": {
        "image_path": "examples/output_dict.png",
        "obj_path": "examples/scene_dict.obj"
    },
    "ray_sampling_rate": 0.01
}

# Parse the config and get the engine
engine = parse_config(config)

# Render the scene
engine.render(
    output_image_path=config['output']['image_path'],
    output_3d_path=config['output'].get('obj_path')
)

print("Rendering complete. Check examples/output_dict.png for the result.")
```

## Development

To install for development:
```bash
git clone https://github.com/KoStard/optics_raytracer
cd optics_raytracer
uv tool install .
```

## License

MIT License
