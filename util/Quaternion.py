import math, numpy as np
from .Angle import Angle
from .Vec3 import Vec3

class Quaternion:
    """
    Quaternion class for 3D rotations and interpolations.
    
    Supports quaternion multiplication, vector rotation, SLERP, and Euler conversions.

    (Use with caution, your keyboard may break from water damage upon use)
    """
    def __init__(self, w=0, x=0, y=0, z=-1):
        # Certainly a quat, init?
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        # Multiply this with that and here with there
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        return Quaternion(w, x, y, z)
    
    def __eq__(self, other):
        # Equality is something quaternions fought for
        return (
            isinstance(other, Quaternion) and
            math.isclose(self.w, other.w) and
            math.isclose(self.x, other.x) and
            math.isclose(self.y, other.y) and
            math.isclose(self.z, other.z)
        )
    
    def __repr__(self):
        return f"(w={self.w}, x={self.x}, y={self.y}, z={self.z})"
    
    def norm(self):
        """Returns the normal of the Quaternion. Much like a magnitude on a Vec3."""
        # It is quite normal
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def conjugate(self):
        """Returns a Quaternion's 'opposite'."""
        # Doesnt that mean to group up?
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def inverse(self):
        """Returns a Quaternion's inverse."""
        # Inversion therapy will be payed for by me
        conjugate = self.conjugate()
        normSquared = self.norm() ** 2
        return Quaternion(
            conjugate.w / normSquared,
            conjugate.x / normSquared,
            conjugate.y / normSquared,
            conjugate.z / normSquared
        )
    
    def normalize(self):
        """Normalizes the Quaternion, in the same way you would a Vec3."""
        # Take the normal and normalize the normal so the normal is normal
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("Cannot normalize a zero length quaternion.")
        
        self.w /= norm
        self.x /= norm
        self.y /= norm
        self.z /= norm
        return self

    def rotateVec(self, other):
        """Rotates a 3d vector around a 4d Quaternion."""
        # Rotate vec? Yeah, its like spinning it on a chair... a 3d chair... a 3d chair with wheels... and wheels drive...
        vecQuat = Quaternion(0, other.x, other.y, other.z)
        result = (self * vecQuat) * self.inverse()
        return Vec3(result.x, result.y, result.z)

    def slerp(self, other, t):
        """
        SLERP (Spherical Linear intERPolation.)
        
        Interpolates new points between two Quaternions based on a t factor.

        0 = no change from original

        0.5 = half way point between original and other

        1 = returns new quat positioned as other
        """
        # SLERP :P
        if not (0 <= t <= 1):
            raise ValueError("t must be range [0, 1].")
        
        dot = self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z
        if dot < 0:
            other = Quaternion(-other.w, -other.x, -other.y, -other.z)
            dot = -dot

        # Quick return if the difference between angles is small enough
        if dot > 0.9995:
            result = Quaternion(
                self.w + t * (other.w - self.w),
                self.x + t * (other.x - self.x),
                self.y + t * (other.y - self.y),
                self.z + t * (other.z - self.z)
            )
            result.normalize()
            return result
        
        theta0    = math.acos(dot)
        sinTheta0 = math.sin(theta0)

        theta     = theta0 * t
        sinTheta  = math.sin(theta)

        s1 = math.cos(theta) - dot * sinTheta / sinTheta0
        s2 = sinTheta / sinTheta0

        return Quaternion(
                self.w * s1 + other.w * s2,
                self.x * s1 + other.x * s2,
                self.y * s1 + other.y * s2,
                self.z * s1 + other.z * s2
        )

    def toMatrix(self) -> np.ndarray:
        """Returns a matrix of the Quaternion, for matrix math..."""
        # Hacking the main frame
        w, x, y, z = self.w, self.x, self.y, self.z
        return np.array([
            [1-2*(y**2 + z**2),   2*(x*y  - z*w ),   2*(x*z  + y*w ), 0],
            [  2*(x*y  + z*w ), 1-2*(x**2 + z**2),   2*(y*z  - x*w ), 0],
            [  2*(x*z  - y*w ),   2*(y*z  + x*w ), 1-2*(x**2 + y**2), 0],
            [                0,                 0,                 0, 1]
        ],dtype=np.float32)

    @staticmethod
    def fromEuler(pitch=0, yaw=0, roll=0):
        """Returns a Quaternion from Euler angles.
         
        Can take an Angle object as inputs, will then use the radian."""
        # Gotta Euler up, or you might end up with a sticky situation... your call.
        if isinstance(pitch, Angle):
            pitch = pitch.radians
        if isinstance(yaw, Angle):
            yaw   = yaw.radians
        if isinstance(roll, Angle):
            roll  = roll.radians

        cy = math.cos(yaw*.5)
        sy = math.sin(yaw*.5)
        
        cp = math.cos(pitch*.5)
        sp = math.sin(pitch*.5)

        cr = math.cos(roll*.5)
        sr = math.sin(roll*.5)

        yQuat = Quaternion(cy, 0, sy,  0)
        pQuat = Quaternion(cp, sp, 0,  0)
        rQuat = Quaternion(cr, 0,  0, sr)

        return yQuat * pQuat * rQuat
