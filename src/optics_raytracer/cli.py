import json
import sys
from pathlib import Path
from typing import Dict, Any
from PIL import Image
from .engine import OpticsRayTracingEngine
from .camera import Camera
from .lens import Lens
from .inserted_image import InsertedImage
from .size import IntegerSize
from .vec3 import Point3, Vec3

def parse_config(config: Dict[str, Any]) -> OpticsRayTracingEngine:
    """Parse JSON config into OpticsRayTracingEngine instance"""
    # Parse camera
    cam_cfg = config['camera']
    camera = Camera(
        Point3(*cam_cfg['center']),
        cam_cfg['focal_distance'],
        IntegerSize(*cam_cfg['viewport_size']).float_scale_to_width(cam_cfg['viewport_width']),
        IntegerSize(*cam_cfg['image_size']),
        Vec3(*cam_cfg['u_vector']),
        Vec3(*cam_cfg['viewport_normal'])
    )

    # Parse hittable objects
    hittables = []
    for obj in config['objects']:
        if obj['type'] == 'lens':
            hittables.append(Lens(
                Point3(*obj['center']),
                obj['radius'],
                Vec3(*obj['normal']),
                obj['focal_distance']
            ))
        elif obj['type'] == 'image':
            image_path = Path(obj['image_path'])
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            image = Image.open(image_path)
            hittables.append(InsertedImage(
                Point3(*obj['left_top']),
                obj['width'],
                IntegerSize(image.width, image.height).float_scale_to_width(obj['width']).height,
                Vec3(*obj['u_vector']),
                Vec3(*obj['normal']),
                image
            ))

    return OpticsRayTracingEngine(
        camera,
        hittables,
        IntegerSize(*cam_cfg['image_size'])
    )

def main():
    if len(sys.argv) != 2:
        print("Usage: optics-raytracer <config.json>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    try:
        with open(config_path) as f:
            config = json.load(f)
        
        engine = parse_config(config)
        engine.render(
            config['output']['image_path'],
            export_3d=config['output'].get('export_3d', False),
            obj_output_path=config['output'].get('obj_path')
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
