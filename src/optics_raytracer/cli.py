import json
import sys
from pathlib import Path
from typing import Dict, Any
from .engine import OpticsRayTracingEngine
from .camera import Camera, FloatSize, IntegerSize, SimpleCamera
from .lens import Lens
from .inserted_image import InsertedImage
import torch
from .torch_details import device

def parse_config(config: Dict[str, Any]) -> OpticsRayTracingEngine:
    """Parse JSON config into OpticsRayTracingEngine instance"""
    # Parse camera
    cam_cfg = config['camera']
    camera = SimpleCamera.build(
        camera_center=torch.tensor(cam_cfg['center'], dtype=torch.float32).to(device),
        focal_distance=cam_cfg['focal_distance'],
        viewport_size=FloatSize.from_width_and_aspect_ratio(
            cam_cfg['viewport_width'],
            IntegerSize(*cam_cfg['image_size']).aspect_ratio
        ),
        image_size=IntegerSize(*cam_cfg['image_size']),
        viewport_u_vector=torch.tensor(cam_cfg['u_vector'], dtype=torch.float32).to(device),
        viewport_normal=torch.tensor(cam_cfg['viewport_normal'], dtype=torch.float32).to(device)
    )

    # Parse objects
    objects = []
    lenses = []
    for obj in config['objects']:
        if obj['type'] == 'lens':
            lenses.append(Lens.build(
                center=torch.tensor(obj['center'], dtype=torch.float32).to(device),
                radius=obj['radius'],
                normal=torch.tensor(obj['normal'], dtype=torch.float32).to(device),
                focal_distance=obj['focal_distance']
            ))
        elif obj['type'] == 'image':
            image_path = Path(obj['image_path'])
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            objects.append(InsertedImage(
                image_path=str(image_path),
                width=obj['width'],
                height=obj.get('height', obj['width']),  # Default to square if height not specified
                middle_point=torch.tensor(obj['center'], dtype=torch.float32).to(device),
                normal=torch.tensor(obj['normal'], dtype=torch.float32).to(device),
                u_vector=torch.tensor(obj['u_vector'], dtype=torch.float32).to(device)
            ))

    return OpticsRayTracingEngine(
        camera=camera,
        objects=objects,
        lenses=lenses,
        ray_sampling_rate_for_3d_export=config.get('ray_sampling_rate', 0.01)
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
            output_image_path=config['output']['image_path'],
            output_3d_path=config['output'].get('obj_path')
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
