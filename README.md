# Optics Raytracer

A 3D optics raytracer for simulating thin lenses and image projection, with OBJ export capabilities.

## Features

- Thin lens simulation with focal distances
- Image projection through lenses
- 3D scene export to OBJ format
- Multiple configuration methods (CLI, Python, JSON)
- Ray visualization in 3D space

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
```json
{
    "camera": {
        "center": [x, y, z],          // Camera position in 3D space
        "focal_distance": 1.0,        // Distance from camera to viewport
        "viewport_width": 2.0,        // Width of viewport in world units
        "image_size": [w, h],         // Output image resolution in pixels
        "u_vector": [x, y, z],        // Right direction vector (typically [1,0,0])
        "viewport_normal": [x, y, z]  // Direction camera is pointing (away from camera)
    },
    "objects": [
        {
            "type": "lens",           // Type of object
            "center": [x, y, z],      // Lens center position
            "radius": 1.0,            // Lens radius
            "normal": [x, y, z],      // Lens orientation (normal vector)
            "focal_distance": -1.0    // Focal length (positive for convex, negative for concave)
        },
        {
            "type": "lens",           // Second lens
            "center": [x, y, z],      
            "radius": 1.0,            
            "normal": [x, y, z],      
            "focal_distance": 1.0     
        },
        {
            "type": "image",          // Type of object
            "left_top": [x, y, z],    // Top-left corner position of image
            "width": 4.0,             // Physical width of image in world units
            "u_vector": [x, y, z],    // Right direction vector of image plane
            "normal": [x, y, z],      // Image plane orientation (normal vector)
            "image_path": "image.png" // Path to source image file
        }
    ],
    "output": {
        "image_path": "output.png",   // Path to save rendered image
        "export_3d": true,            // Whether to export 3D scene
        "obj_path": "scene.obj"       // Path to save 3D scene (if export_3d is true)
    }
}
```

### Configuration Attributes Explained

#### Camera Settings
- **center**: The 3D position of the camera in world coordinates (x,y,z)
- **focal_distance**: Distance from camera to the viewport plane
- **viewport_width**: Alternative way to specify viewport width (height calculated automatically)
- **image_size**: Resolution of output image in pixels (width, height)
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
  - **position**: Top-left corner position of image in 3D space
  - **width**: Physical width of image in world units
  - **u_vector**: Right direction vector of image plane
  - **normal**: Orientation of image plane (normal vector)
  - **image_path**: Path to source image file

#### Output Settings
- **image_path**: Path to save rendered output image
- **export_3d**: Whether to export 3D scene (true/false)
- **obj_path**: Path to save 3D scene file (if export_3d is true)

#### Examples

Example config files are available in the `examples/` directory. Run them with:

```bash
# Run telescope example
optics-raytracer examples/telescope.json

# Run microscope example 
optics-raytracer examples/microscope.json
```
Some ready examples to check:
- [Simple Demo With Convex and Concave Lenses](https://3dviewer.net/index.html#model=https://raw.githubusercontent.com/KoStard/optics_raytracer/refs/heads/master/scene.obj)
- [Simple Telescope](https://3dviewer.net/#model=https://raw.githubusercontent.com/KoStard/optics_raytracer/refs/heads/master/telescope_scene.obj)
- [Simple Microscope](https://3dviewer.net/#model=https://raw.githubusercontent.com/KoStard/optics_raytracer/refs/heads/master/microscope_scene.obj)

Notice that not all rays and hits are rendered in the OBJ to keep the file light. The rendered ones are chosen randomly.

### 2. Python Configuration

```python
from optics_raytracer import (
    OpticsRayTracingEngine, Camera, Lens, InsertedImage,
    IntegerSize, Point3, Vec3
)
from PIL import Image

# Setup camera
camera = Camera(
    Point3(0, 0, 0), 
    1,
    IntegerSize(400, 225).float_scale_to_width(2),
    IntegerSize(400, 225),
    Vec3(1, 0, 0),
    Vec3(0, 0, -1)
)

# Load image and create objects
image = Image.open("image.png")
inserted_image = InsertedImage(
    Point3(-2, 1, -4),
    4,
    IntegerSize(image.width, image.height).float_scale_to_width(4).height,
    Vec3(1, 0, 0),
    Vec3(0, 0, -1),
    image
)

lens1 = Lens(Point3(0, 0, -2), 1, Vec3(0, 0, -1), -1)
lens2 = Lens(Point3(0, 0, -3), 1, Vec3(0, 0, -1), 1)

# Create and run engine
engine = OpticsRayTracingEngine(
    camera,
    [lens1, lens2, inserted_image],
    IntegerSize(400, 225)
)
engine.render('output.png', export_3d=True, obj_output_path='scene.obj')
```

### 3. Dictionary Configuration from Python

```python
from optics_raytracer import parse_config

config = {
    "camera": {
        "center": [0, 0, 0],
        "focal_distance": 1,
        "viewport_width": 2,
        "image_size": [400, 225],
        "u_vector": [1, 0, 0],
        "viewport_normal": [0, 0, -1]
    },
    "objects": [
        {
            "type": "lens",
            "center": [0, 0, -2],
            "radius": 1,
            "normal": [0, 0, -1],
            "focal_distance": -1
        },
        {
            "type": "image",
            "position": [-2, 1, -4],
            "width": 4,
            "u_vector": [1, 0, 0],
            "normal": [0, 0, -1],
            "image_path": "image.png"
        }
    ],
    "output": {
        "image_path": "output.png",
        "export_3d": True,
        "obj_path": "scene.obj"
    }
}

engine = parse_config(config)
engine.render('output.png', export_3d=True, obj_output_path='scene.obj')
```

## Development

To install for development:
```bash
git clone https://github.com/KoStard/optics_raytracer
cd optics_raytracer
uv pip install -e .
```

## License

MIT License
