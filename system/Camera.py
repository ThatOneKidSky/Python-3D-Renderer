from util import Vec3, Quaternion

class Camera:
    """A bare bones Camera, it really is shrimple tho."""
    def __init__(self, position:Vec3, rotation:Quaternion):
        self.position = position
        self.rotation = rotation
        self.calculateCameraVectors()
    
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

    #endregion
