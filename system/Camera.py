from util import Vec3, Quaternion
import numpy as np, math, SETTINGS

class Camera:
    """A bare bones Camera, it really is shrimple tho."""
    def __init__(self, position:Vec3, rotation:Quaternion, FOV:int = 45):
        self.position = position
        self.rotation = rotation
        self.calculateCameraVectors()
        
        self.FOV  = FOV
        self.NEAR = 0.1
        self.FAR  = 100.0

        self.viewMatrix       = self.getViewMatrix()
        self.projectionMatrix = self.getProjectionMatrix()
    
    #region Directions Vectors
    def calculateCameraVectors(self):
        """Recalculates all direction vectors and sets them. Returns nothing."""
        self.forward = self.forwardVector()
        self.up      = self.upVector()
        self.right   = self.rightVector()

    def forwardVector(self):
        """Returns the forward vector"""
        return self.rotation.rotateVec(Vec3(0, 0, -1))
    
    def upVector(self):
        """Returns the up vector"""
        return self.rotation.rotateVec(Vec3(0, 1, 0))
    
    def rightVector(self):
        """Returns the right vector"""
        return self.rotation.rotateVec(Vec3(1, 0, 0))
    #endregion

    #region Positioning
    def rotate(self, *angle):
        """
        Rotates the camera based on either a Quaternion object, 
        
        or Euler angles in the order of [pitch, yaw, roll] (will default to 0)
        """
        if isinstance(angle[0], Quaternion):
            rotationQuat = angle[0]
        else:
            pitch = angle[0] if angle[0] is not None else 0
            yaw   = angle[1] if angle[1] is not None else 0
            roll  = angle[2] if angle[2] is not None else 0
            
            rotationQuat = Quaternion.fromEuler(pitch, yaw, roll)
        
        self.rotation *= rotationQuat
        self.calculateCameraVectors()

        self.viewMatrix       = self.getViewMatrix()
        self.projectionMatrix = self.getProjectionMatrix()

    #endregion

    def getViewMatrix(self):
        f = self.forward
        r = self.right
        u = self.up
        p = self.position

        return np.array([
            [ r.x,  r.y,  r.z, -r.dot(p)],
            [ u.x,  u.y,  u.z, -u.dot(p)],
            [-f.x, -f.y, -f.z,  f.dot(p)],
            [   0,    0,    0,         1],
        ],dtype=np.float32)
    
    def getProjectionMatrix(self):
        fovRad = math.radians(self.FOV)
        f = 1 / math.tan(fovRad / 2)
        fa = f / SETTINGS.SCREEN.ASPECT
        fp1 = (self.NEAR + self.FAR) / (self.NEAR - self.FAR)
        fp2 = (2 * self.FAR * self.NEAR) / (self.NEAR - self.FAR)
        return np.array([
            fa, 0,   0,   0,
             0, f,   0,   0,
             0, 0, fp1, fp2,
             0, 0,  -1,   0,
        ])