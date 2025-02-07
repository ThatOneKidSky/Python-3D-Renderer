import math

class Angle:
    """
    An object used for handling angles.
    
    Built in sin, cos, tan, and normalize function.
    
    (value does not normalize when adding or subtracting)
    """
    def __init__(self, radians=0, degrees=0):
        if radians and degrees:
            raise ValueError("Cannot specify both radians and degrees")

        if radians:
            self.radians = radians
            self.degrees = math.degrees(radians)
        elif degrees:
            self.radians = math.radians(degrees)
            self.degrees = degrees
        else:
            self.radians = 0
            self.radians = 0
    
    def __repr__(self):
        return f"Angle(radians={self.radians}, degrees={self.degrees})"
    
    def __str__(self):
        return f"{self.radians}"

    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(radians=self.radians + other.radians)
        raise TypeError("Can only add another Angle.")

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(radians=self.radians - other.radians)
        raise TypeError("Can only subtract another Angle.")
    
    def sin(self):
        """Returns the sine of the angle."""
        return math.sin(self.radians)
    
    def cos(self):
        """Returns the cosine of the angle."""
        return math.cos(self.radians)
    
    def tan(self):
        """Returns the tangent of the angle."""
        return math.tan(self.radians)
    
    def normalize(self):
        """Normalizes the angle between 0 and 360 degrees (0-2pi radians)"""
        self.degrees = self.degrees % 360
        self.radians = math.radians(self.degrees)
