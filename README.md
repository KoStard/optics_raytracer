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
        "center": [0, 0, 0],
        "focal_distance": 1,
        "viewport_size": [400, 225],
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
        "export_3d": true,
        "obj_path": "scene.obj"
    }
}
```

Run the raytracer:
```bash
optics-raytracer config.json
```

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
        "viewport_size": [400, 225],
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
