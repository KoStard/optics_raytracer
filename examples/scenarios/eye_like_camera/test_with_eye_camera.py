import numpy as np
from optics_raytracer.camera import EyeCamera, FloatSize, IntegerSize
from optics_raytracer.lens import Lens
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.engine import OpticsRayTracingEngine

# In decimeter
lens_focal_distance = 0.24

# while True:
if True:
    # Create eye camera
    camera = EyeCamera.build(
        viewport_center=np.array([0, 0, 0], dtype=np.float32),
        lens_distance=0.24,
        lens_radius=0.01,
        number_of_circles=2,
        rays_per_circle=5,
        viewport_size=FloatSize(0.35, 0.35),
        image_size=IntegerSize(400, 400),
        viewport_u_vector=np.array([1, 0, 0], dtype=np.float32),
        viewport_normal=np.array([0, 0, -1], dtype=np.float32),
        lens_focal_distance=lens_focal_distance,
    )

    # BUG: normal impacting focal distance - lens are same from both sides
    # Create a lens
    lens = Lens.build(
        center=np.array([5, 0, -10], dtype=np.float32),
        radius=5.0,
        normal=np.array([0, 0, -1], dtype=np.float32),
        focal_distance=2.0,
    )

    # Create an image from image.png
    # TODO: Another bug: image distance issues:
    """
    width=100.0,
    height=100.0,
    middle_point=np.array([0, 0, -200], dtype=np.float32),
    """
    image = InsertedImage(
        image_path="examples/assets/image.png",
        width=50.0,
        height=50.0,
        middle_point=np.array([0, 0, -50], dtype=np.float32),
        normal=np.array([0, 0, -1], dtype=np.float32),
        u_vector=np.array([1, 0, 0], dtype=np.float32),
    )
    apple = InsertedImage(
        image_path="examples/assets/apple.png",
        width=0.3,
        height=0.3,
        middle_point=np.array([0.2, 0, -0.6], dtype=np.float32),
        normal=np.array([0, 0, -1], dtype=np.float32),
        u_vector=np.array([1, 0, 0], dtype=np.float32),
    )

    # Create ray tracing engine
    engine = OpticsRayTracingEngine(
        camera=camera,
        objects=[image, apple],
        lenses=[
            # lens
        ],
        ray_sampling_rate_for_3d_export=0.01,
    )

    # Render the scene
    engine.render(
        output_image_path="examples/scenarios/eye_like_camera/test_with_eye.png",
        output_3d_path="examples/scenarios/eye_like_camera/test_with_eye.obj",
        output_mtl_path="examples/scenarios/eye_like_camera/test_with_eye.mtl",
    )
    print(f"Done for lens focal distance {lens_focal_distance}")

    # key = input("Press + or - to adjust the focal distance by 0.05, or enter number: ")
    # if key == "+":
    #     lens_focal_distance += 0.05
    # elif key == "-":
    #     lens_focal_distance -= 0.05
    # else:
    #     lens_focal_distance = float(key)
