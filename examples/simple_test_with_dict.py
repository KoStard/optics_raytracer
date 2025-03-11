from optics_raytracer.cli import parse_config

# Define the scene using a dictionary (similar to JSON structure
config = {
    "camera": {
        "center": [0, 0, 0],
        "focal_distance": 1.0,
        "viewport_width": 2.0,
        "image_size": [1600, 1600],
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