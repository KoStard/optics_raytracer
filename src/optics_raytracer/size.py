class IntegerSize:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
    
    @property
    def aspect_ratio(self):
        return self.width / self.height
    
    @classmethod
    def from_width_and_aspect_ratio(cls, width, aspect_ratio):
        return cls(width, max(width // aspect_ratio, 1))
    
    def float_scale(self, scale):
        return FloatSize(self.width * scale, self.height * scale)
    
    def float_scale_to_width(self, width):
        return self.float_scale(width / self.width)
    
    def __str__(self):
        return f"{self.width}x{self.height}"

class FloatSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def aspect_ratio(self):
        return self.width / self.height
    
    @classmethod
    def from_width_and_aspect_ratio(cls, width, aspect_ratio):
        return cls(width, width / aspect_ratio)
    
    def scale(self, scale):
        return FloatSize(self.width * scale, self.height * scale)
    
    def scale_to_width(self, width):
        return self.scale(width / self.width)

    def __str__(self):
        return f"{self.width}x{self.height}"

    def to_int_size(self):
        return IntegerSize(int(self.width), int(self.height))