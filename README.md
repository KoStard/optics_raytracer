# Optics Raytracer

A 3D optics raytracer for simulating thin lenses and image projection, with OBJ export capabilities.

## Features

- Thin lens simulation with focal distances
- Image projection through lenses
- Ray visualization in 3D space
- 3D scene export to OBJ format
- Clear group naming in OBJ files
- Multiple configuration methods (CLI, Python, JSON)

![Board](https://github.com/user-attachments/assets/44d65d6f-788d-4c75-894c-392aa97065a2)

3D Examples:
- [telescope_scene](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/astronomical_telescope/telescope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/astronomical_telescope/telescope_scene.obj)
- [compound_microscope_scene](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/compound_microscope/compound_microscope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/compound_microscope/compound_microscope_scene.obj)
- [test_with_eye](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/eye_like_camera/test_with_eye.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/eye_like_camera/test_with_eye.obj)
- [microscope_scene](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/microscope/microscope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/microscope/microscope_scene.obj)
- [prismatic_effect_scene](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/prismatic_effect/prismatic_effect_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/prismatic_effect/prismatic_effect_scene.obj)
- [telescope_scene](https://3dviewer.net/#model=https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/telescope/telescope_scene.mtl,https://github.com/KoStard/optics_raytracer/blob/master/examples/scenarios/telescope/telescope_scene.obj)

![lens_comparison](https://github.com/user-attachments/assets/dd0346bd-d602-4f47-b9b0-bf974147b808) ![moving_lens](https://github.com/user-attachments/assets/e56c2415-84a1-4687-a9a3-fc2c78a55d88)

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

The CLI tool can process one or multiple JSON configuration files:

```bash
# Process a single config file
optics-raytracer config.json

# Process multiple config files sequentially
optics-raytracer config1.json config2.json config3.json
```

Create a config.json file:
```python
{
    "camera": {
        // Simple camera (default)
        "type": "simple",             # Camera type: "simple" or "eye"
        "center": [x, y, z],          # Camera position in 3D space
        "focal_distance": 1.0,        # Distance from camera to viewport
        "viewport_width": 2.0,        # Width of viewport in world units
        "image_size": [w, h],         # Output image resolution in pixels
        "u_vector": [x, y, z],        # Right direction vector (typically [1,0,0])
        "viewport_normal": [x, y, z]  # Direction camera is pointing (away from camera)
        
        // Or eye-like camera
        "type": "eye",                # Camera type: "simple" or "eye"
        "center": [x, y, z],          # Viewport center position
        "lens_distance": 1.0,         # Distance from viewport to lens
        "lens_radius": 0.5,           # Radius of the lens
        "lens_focal_distance": 0.24,  # Focal distance of the lens
        "number_of_circles": 2,       # Number of concentric sampling circles on lens (optional, default: 2)
        "rays_per_circle": 3,         # Rays per sampling circle (optional, default: 5)
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

##### Simple Camera (default)
- **type**: Camera type, set to "simple" or omit for simple camera
- **center**: The 3D position of the camera in world coordinates (x,y,z)
- **focal_distance**: Distance from camera to the viewport plane
- **viewport_width**: Width of viewport in world units (height calculated based on aspect ratio)
- **image_size**: Resolution of output image in pixels [width, height]
- **u_vector**: Right direction vector of the camera (typically [1,0,0])
- **viewport_normal**: Direction the camera is pointing (normal vector away from camera)

##### Eye-like Camera
- **type**: Camera type, set to "eye" for eye-like camera with lens
- **center**: The 3D position of the viewport in world coordinates (x,y,z)
- **lens_distance**: Distance from viewport to lens (in decimeters)
- **lens_radius**: Physical radius of the lens
- **lens_focal_distance**: Focal distance of the lens (in decimeters)
- **object_distance**: Alternative to lens_focal_distance - Distance to the object that should be in focus (in decimeters)
- **number_of_circles**: Number of concentric sampling circles on lens (optional, default: 2) 
- **rays_per_circle**: Number of rays per sampling circle (optional, default: 5)

  Note: For eye-like camera, provide either `lens_focal_distance` OR `object_distance`, not both. To focus at infinity, use `lens_focal_distance` equal to `lens_distance`.
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
  - **focal_distance**: Focal length in decimeters (positive for convex, negative for concave lenses)
  - **magnification**: Alternative to focal_distance - Magnifying power of the lens (M = 1 + 2.5/f, where f is focal length in decimeters)
  
  Note: For lenses, provide either `focal_distance` OR `magnification`, not both.
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
- **include_missed_rays**: If true, includes rays that don't hit any object or lens in the 3D export (optional, default is false)

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
from optics_raytracer import SimpleCamera, FloatSize, IntegerSize, Lens, InsertedImage, OpticsRayTracingEngine

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
from optics_raytracer import parse_config

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
