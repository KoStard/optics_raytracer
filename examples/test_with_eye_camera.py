import torch
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine
from optics_raytracer.torch_details import device

# In decimeter
lens_focal_distance = 0.24

# while True:
if True:
    # Create eye camera
    camera = EyeCamera.build(
        viewport_center=torch.tensor([0, 0, 0], dtype=torch.float32).to(device),
        lens_distance=0.24,
        lens_radius=.01,
        number_of_circles=2,
        rays_per_circle=5,
        viewport_size=FloatSize(.35, .35),
        image_size=IntegerSize(400, 400),
        viewport_u_vector=torch.tensor([1, 0, 0], dtype=torch.float32).to(device),
        viewport_normal=torch.tensor([0, 0, -1], dtype=torch.float32).to(device),
        lens_focal_distance=lens_focal_distance
    )

    # BUG: normal impacting focal distance - lens are same from both sides
    # Create a lens
    lens = Lens.build(
        center=torch.tensor([5, 0, -10], dtype=torch.float32).to(device),
        radius=5.0,
        normal=torch.tensor([0, 0, -1], dtype=torch.float32).to(device),
        focal_distance=2.0
    )

    # Create an image from image.png
    # TODO: Another bug: image distance issues:
    """
    width=100.0,
    height=100.0,
    middle_point=torch.tensor([0, 0, -200], dtype=torch.float32).to(device),
    """
    image = InsertedImage(
        image_path="examples/image.png",
        width=50.0,
        height=50.0,
        middle_point=torch.tensor([0, 0, -50], dtype=torch.float32).to(device),
        normal=torch.tensor([0, 0, -1], dtype=torch.float32).to(device),
        u_vector=torch.tensor([1, 0, 0], dtype=torch.float32).to(device)
    )
    apple = InsertedImage(
        image_path="examples/apple.png",
        width=0.3,
        height=0.3,
        middle_point=torch.tensor([0.2, 0, -0.6], dtype=torch.float32).to(device),
        normal=torch.tensor([0, 0, -1], dtype=torch.float32).to(device),
        u_vector=torch.tensor([1, 0, 0], dtype=torch.float32).to(device)
    )

    # Create ray tracing engine
    engine = OpticsRayTracingEngine(
        camera=camera,
        objects=[image, apple],
        lenses=[
            # lens
            ],
        ray_sampling_rate_for_3d_export=0.01
    )

    # Render the scene
    engine.render(
        output_image_path="examples/test_with_eye.png",
        output_3d_path="examples/test_with_eye.obj"
    )
    print(f"Done for lens focal distance {lens_focal_distance}")
    
    # key = input("Press + or - to adjust the focal distance by 0.05, or enter number: ")
    # if key == "+":
    #     lens_focal_distance += 0.05
    # elif key == "-":
    #     lens_focal_distance -= 0.05
    # else:
    #     lens_focal_distance = float(key)
