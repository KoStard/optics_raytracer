"""
Helper module for consistent group naming throughout the application.
"""


class GroupNamer:
    """
    Creates consistent, descriptive group names for various elements
    in optical simulations.
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
        suffix = GroupNamer.get_ordinal_suffix(num)
        return f"{num}{suffix}"

    # Ray Group Names
    @staticmethod
    def get_primary_rays():
        """Returns name for primary rays group"""
        return "🌟 Primary Rays"
    
    @staticmethod
    def get_refraction_rays(depth):
        """Returns name for refraction rays group of specified depth"""
        ordinal = GroupNamer.get_ordinal(depth)
        return f"🔄 {ordinal} Refraction"
    
    @staticmethod
    def get_missed_rays():
        """Returns name for missed rays group"""
        return "❌ Missed Rays"
        
    @staticmethod
    def get_camera_internal_rays():
        """Returns name for camera internal rays group"""
        return "🔍 Camera Internal Rays"
        
    # Object Outlines 
    @staticmethod
    def get_lens_outlines():
        """Returns name for lens outlines group"""
        return "🔵 Lens Outlines"
        
    @staticmethod
    def get_screen_outlines():
        """Returns name for screen/rectangle outlines group"""
        return "🟢 Screen Outlines"
    
    # Hit Points
    @staticmethod
    def get_camera_lens_intersection():
        """Returns name for camera lens intersection points"""
        return "📸 Camera Lens Intersection"
        
    @staticmethod
    def get_hit_points():
        """Returns name for generic hit points"""
        return "📌 Hit Points"
        
    @staticmethod
    def get_lens_hit_points(lens_index):
        """Returns name for lens hit points with index"""
        return f"📍 Lens {lens_index} Hits"
        
    @staticmethod
    def get_object_hit_points(object_index):
        """Returns name for object hit points with index"""
        return f"🎯 Object {object_index} Hits"

    # Legacy methods for backward compatibility    
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
        # Base prefixes for different depths with emojis
        if depth is None:
            prefix = GroupNamer.get_primary_rays()
        else:
            prefix = GroupNamer.get_refraction_rays(depth)

        # Add object information
        if hit_object_type == "lens" and hit_object_index is not None:
            return f"{prefix} → 🔍 Lens {hit_object_index}"
        elif hit_object_type == "object" and hit_object_index is not None:
            return f"{prefix} → 🎯 Object {hit_object_index}"
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
            return GroupNamer.get_lens_hit_points(hit_object_index)
        elif hit_object_type == "object" and hit_object_index is not None:
            return GroupNamer.get_object_hit_points(hit_object_index)
        else:
            return GroupNamer.get_hit_points()
