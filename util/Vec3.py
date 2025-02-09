import math
from .clamp import clamp
from .Angle import Angle

class Vec3:
    """
    A 3D vector class that can handle:

    - Dot product (self.dot)
    - Element wise multiplication (self.elementWise)
    - Magnitude (self.magnitude)
    - Normalize (self.normalize)
    - Angle between (self.angleBetween)
    - Cross product (self.cross)
    - Lerp (self.lerp)
    - Reflection (self.reflect)
    - Scaling (self.scale)
    - Clamping (self.clamp)
    """
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        # Represent yourself, in string...
        return f"(x={self.x}, y={self.y}, z={self.z})"
    
    def __str__(self):
        # Im just stringing it together at this point
        return f"({round(self.x,2)}, {round(self.y,2)}, {round(self.z,2)})"
    
    def __add__(self, other):
        # Direction plus direction, whats not to understand?
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError("Can only add Vec3 to Vec3")
    
    def __sub__(self, other):
        # Its like adding, but backwards
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError("Can only subtract Vec3 from Vec3")

    def __mul__(self, other):
        # Makes your vector stronger, it wont make you stronger tho
        if isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        raise TypeError("Can only multiply Vec3 by a number")
    
    def __rmul__(self, other):
        # Its real multipication, its real because it copies others
        return self.__mul__(other)
    
    def __truediv__(self, other):
        # Its multiplication, but backwards
        if isinstance(other, (int, float)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        raise TypeError("Can only divide Vec3 by a number")

    def dot(self, other):
        """Returns the dot product of vectors."""
        # Bassically adds two vectors, and then flattens them down
        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        raise TypeError("Other must be a Vec3")
    
    def elementWise(self, other):
        """Returns the element wise multiplication of vectors."""
        # Adding more bricks to a vector based on another vector, each set sold separately
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise TypeError("Other must be a Vec3")

    def magnitude(self):
        """Calculates the magnitude or length of the vector."""
        # My vector is far, what about yours?
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def normalize(self):
        """Returns a normalized version of the vector."""
        # Return to start, dont collect lerps
        mag = self.magnitude()
        if mag == 0:
            return Vec3(0, 0, 0)
        return Vec3(self.x / mag, self.y / mag, self.z / mag)
    
    def angleBetween(self, other):
        """Returns the angle between two vectors."""
        # Between two worlds lies a place where letters didnt get put in math
        if isinstance(other, Vec3):
            dot = self.dot(other)
            mag = self.magnitude() * other.magnitude()
            cos = clamp(dot / mag, -1, 1)
            rad = math.acos(cos)
            return Angle(radians=rad)
        raise TypeError("Other must be a Vec3")
    
    def cross(self, other):
        """Returns the cross product of vectors."""
        # You crossed the wrong vector foo
        if isinstance(other, Vec3):
            return Vec3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        raise TypeError("Other must be a Vec3")

    def lerp(self, other, t):
        """LERP. Returns the lerped vector."""
        # LERP
        if isinstance(other, Vec3):
            if isinstance(t, (int, float)):
                t = clamp(t, 0, 1)
                return Vec3(
                    self.x + t * (other.x - self.x),
                    self.y + t * (other.y - self.y),
                    self.z + t * (other.z - self.z),
                )
            raise TypeError("(t) must be a number")
        raise TypeError("Other must be a Vec3")
    
    def reflect(self, other):
        """Reflects the vector across another vector."""
        # A mirror function. Whens the last time you looked in a mirror?
        if isinstance(other, Vec3):
            dot = self.dot(other)
            return Vec3(
                self.x - 2 * dot * other.x,
                self.y - 2 * dot * other.y,
                self.z - 2 * dot * other.z,
            )
        raise TypeError("Other must be a Vec3")
    
    def scale(self, other):
        """Scale the vector by a number."""
        # Scale, not scale, nor scale, neither scale, and never scale.
        if isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        raise TypeError("Other must be an int or float")

    def clamp(self, minVal, maxVal):
        """Clamps the magnitude of the vector to be between min and max."""
        # If your vector is to far from a space, clamp that baby. (dont clamp babies)
        if isinstance(minVal, (int, float)):
            if isinstance(maxVal, (int, float)):
                mag = self.magnitude()
                if mag < minVal:
                    return self.scale(minVal / mag)
                elif mag > maxVal:
                    return self.scale(maxVal / mag)
                return self
            raise TypeError("MaxVal must be an int or float")
        raise TypeError("MinVal must be an int or float")
    

