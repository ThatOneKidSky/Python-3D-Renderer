import math
from .Angle import Angle
from .clamp import clamp
from .Vec3 import Vec3

def matrix(A, B):
    if isinstance(A, Vec3):
        A = [[A.x, A.y, A.z]]
        
    if isinstance(B, Vec3):
        B = [
            [B.x, 0,   0  ],
            [0,   B.y, 0  ],
            [0,   0,   B.z]
        ]

    if len(A[0]) != len(B):
        raise ValueError("Matrices have incompatible dimentions.")
    
    result = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))
    
    return result

class Vec2:
    """
    A 2D vector class that can handle:

    - Dot product (self.dot)
    - Element wise multiplication (self.elementWise)
    - Magnitude (self.magnitude)
    - Normalize (self.normalize)
    - Angle (self.angle)
    - Angle between (self.angleBetween)
    - Normal (self.normal)
    - Lerp (self.lerp)
    - Reflection (self.reflect)
    - Scaling (self.scale)
    - Clamping (self.clamp
    """
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vec2(x={self.x}, y={self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vec2 to Vec2")
    
    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        raise TypeError("Can only subtract Vec2 from Vec2")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        raise TypeError("Can only multiply Vec2 by a number")
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        raise TypeError("Can only divide Vec2 by a number")

    def dot(self, other):
        """Returns the dot product of vectors."""
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        raise TypeError("Other must be a Vec2")
    
    def elementWise(self, other):
        """Returns the element wise multiplication of vectors."""
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        raise TypeError("Other must be a Vec2")

    def magnitude(self):
        """Calculates the magnitude of the vector."""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        """Returns a normalized version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vec2(0, 0)
        return Vec2(self.x / mag, self.y / mag)
    
    def angle(self):
        """Returns the angle of the vector."""
        return Angle(math.atan2(self.x, self.y))
    
    def angleBetween(self, other):
        """Returns the angle between two vectors."""
        if isinstance(other, Vec2):
            dot = self.dot(other)
            mag = self.magnitude() * other.magnitude()
            cos = clamp(dot / mag, -1, 1)
            rad = math.acos(cos)
            return Angle(radians=rad)
        raise TypeError("Other must be a Vec2")
    
    def normal(self):
        """Returns the normal vector."""
        return Vec2(-self.y, self.x)
    
    def lerp(self, other, t):
        """LERP. Returns the lerped vector."""
        if isinstance(other, Vec2):
            if isinstance(t, (int, float)):
                t = clamp(t, 0, 1)
                return Vec2(self.x + t * (other.x - self.x), self.y + t * (other.y - self.y))
            raise TypeError("(t) must be a number")
        raise TypeError("Other must be a Vec2")
    
    def reflect(self, other):
        """Reflects the vector across another vector."""
        dot = self.dot(other)
        return Vec2(self.x - 2 * dot * other.x, self.y - 2 * dot * other.y)
    
    def scale(self, other):
        """Scale the vector by a number."""
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        raise TypeError("Other must be an int or float")

    def clamp(self, minVal, maxVal):
        """Clamps the magnitude of the vector to be between min and max."""
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
