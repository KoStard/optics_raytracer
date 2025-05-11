"""
Helper module for consistent ray group naming throughout the application.
"""


class RayGroupNamer:
    """
    Creates consistent, descriptive group names for rays interacting with
    different objects in optical simulations.
    """

    @staticmethod
    def get_ordinal_suffix(num):
        """
        Returns the ordinal suffix for a number (1st, 2nd, 3rd, etc.)
        """
        if 10 <= num % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
        return suffix

    @staticmethod
    def get_ordinal(num):
        """
        Returns the full ordinal representation of a number (1st, 2nd, 3rd, etc.)
        """
        suffix = RayGroupNamer.get_ordinal_suffix(num)
        return f"{num}{suffix}"

    @staticmethod
    def get_ray_group_name(depth=None, hit_object_type=None, hit_object_index=None):
        """
        Get a consistent group name for rays based on their characteristics.
        
        Args:
            depth: The interaction depth (refraction count) of the ray
            hit_object_type: Type of object hit ("lens" or "object")
            hit_object_index: Index of the hit object
            
        Returns:
            A descriptive and consistent group name string
        """
        # Base prefixes for different depths
        if depth is None:
            prefix = "primary_rays"
        else:
            ordinal = RayGroupNamer.get_ordinal(depth)
            prefix = f"{ordinal}_refraction"
        
        # Add object information
        if hit_object_type == "lens" and hit_object_index is not None:
            return f"{prefix}_through_lens_{hit_object_index}"
        elif hit_object_type == "object" and hit_object_index is not None:
            return f"{prefix}_at_object_{hit_object_index}"
        else:
            return prefix

    @staticmethod
    def get_hit_point_group_name(hit_object_type=None, hit_object_index=None):
        """
        Get a consistent group name for hit points based on their characteristics.
        
        Args:
            hit_object_type: Type of object hit ("lens" or "object")
            hit_object_index: Index of the hit object
            
        Returns:
            A descriptive and consistent group name string
        """
        if hit_object_type == "lens" and hit_object_index is not None:
            return f"hit_points_at_lens_{hit_object_index}"
        elif hit_object_type == "object" and hit_object_index is not None:
            return f"hit_points_at_object_{hit_object_index}"
        else:
            return "hit_points"
