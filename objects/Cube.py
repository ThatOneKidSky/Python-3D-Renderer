from util import *
import numpy as np
from .RootObject import RootObject

class Cube(RootObject):
    s = 0.5
    verticies = np.array([
        # X Y Z      X Y Z
        # Front
        -s,  s,  s, -np.sqrt(2),  np.sqrt(2),  np.sqrt(2), # 0 Top Left
         s,  s,  s,  np.sqrt(2),  np.sqrt(2),  np.sqrt(2), # 1 Top Right
        -s, -s,  s, -np.sqrt(2), -np.sqrt(2),  np.sqrt(2), # 2 Bottom Left
         s, -s,  s,  np.sqrt(2), -np.sqrt(2),  np.sqrt(2), # 3 Bottom Right
        # Back
        -s,  s, -s, -np.sqrt(2),  np.sqrt(2), -np.sqrt(2), # 4 Top Left
         s,  s, -s,  np.sqrt(2),  np.sqrt(2), -np.sqrt(2), # 5 Top Right
        -s, -s, -s, -np.sqrt(2), -np.sqrt(2), -np.sqrt(2), # 6 Bottom Left
         s, -s, -s,  np.sqrt(2), -np.sqrt(2), -np.sqrt(2), # 7 Bottom Right
    ],dtype=np.float32)
    indices = np.array([
        # Front
        0, 2, 1,   2, 3, 1,
        # Back
        5, 6, 4,   5, 7, 6,
        # Right
        1, 3, 5,   3, 7, 5,
        # Left
        4, 6, 0,   6, 2, 0,
        # Top
        4, 0, 5,   0, 1, 5,
        # Bottom
        2, 6, 3,   6, 7, 3,
    ],dtype=np.uint32)
    stride = 6

    def __init__(self, position=Vec3(), rotation=Quaternion(), scale=Vec3(1,1,1)):
        super().__init__(position, rotation, scale)
    
        self.setup(self.verticies, self.indices, self.stride)
    
    def render(self):
        super().render(self.indices)