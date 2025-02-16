from .rectangle import Rectangle


class PixelatedViewport(Rectangle):
    def __init__(self, left_top, width, height, u_vector, normal, pixel_columns, pixel_rows):
        super().__init__(left_top, width, height, u_vector, normal)
        self.pixel_columns = pixel_columns
        self.pixel_rows = pixel_rows
        self.pixel_width = width / pixel_columns
        self.pixel_height = height / pixel_rows
        self.pixel_distance_u_vector = self.u * self.pixel_width
        self.pixel_distance_v_vector = self.v * self.pixel_height
        self.left_top_pixel_point = self.left_top + self.pixel_distance_u_vector / 2 + self.pixel_distance_v_vector / 2
        
    def get_pixel_point(self, column, row):
        return self.left_top_pixel_point + self.pixel_distance_u_vector * column + self.pixel_distance_v_vector * row

    def convert_point_to_pixel(self, point):
        # Using estimation
        to_point_vec = point - self.left_top_pixel_point
        column = round(to_point_vec.dot(self.u) / self.pixel_width)
        row = round(to_point_vec.dot(self.v) / self.pixel_height)
        return column, row
