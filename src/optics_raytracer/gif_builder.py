class GifBuilder:
    """
    Class for building and saving animated GIFs from a sequence of images.
    Provides optimization options for smaller file sizes.
    """

    def __init__(self, optimize=True, duration=100):
        """
        Initialize the GIF builder.

        Args:
            optimize: Whether to optimize the GIF for file size (default: True)
            duration: Duration of each frame in milliseconds (default: 100)
        """
        self.images = []
        self.optimize = optimize
        self.duration = duration

    def add_image(self, image):
        """
        Add an image to the GIF sequence.

        Args:
            image: PIL Image object to add to the sequence
        """
        # Convert to RGB mode if needed to ensure consistency
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Make a copy to avoid modifying the original
        self.images.append(image.copy())

    def save(self, filepath):
        """
        Save the sequence of images as an animated GIF.

        Args:
            filepath: Path where the GIF will be saved
        """
        if not self.images:
            raise ValueError("No images added to the GIF builder")

        # Save the first image as the base, then append the rest
        first_image = self.images[0]
        remaining_images = self.images[1:] if len(self.images) > 1 else []

        first_image.save(
            filepath,
            save_all=True,
            append_images=remaining_images,
            optimize=self.optimize,
            duration=self.duration,
            loop=0,  # Loop forever
        )

        return filepath
