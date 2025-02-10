import numpy as np
from util import Vec3, Quaternion
from OpenGL.GL import *

class RootObject:
    def __init__(self, position=Vec3(), rotation=Quaternion(), scale=Vec3(1,1,1)):
        self.position = position
        self.rotation = rotation
        self.scale    = scale

        self.modelMatrix  = None
        self.matrixUpdate = True

        self.VAO = None
        self.VBO = None
        self.EBO = None

    def getModelMatrix(self):
        if self.matrixUpdate:
            p = self.position
            r = self.rotation.toMatrix()
            s = self.scale
            self.modelMatrix = np.array([
                [s.x*r[0,0], s.x*r[0,1], s.x*r[0,2], p.x],
                [s.y*r[1,0], s.y*r[1,1], s.y*r[1,2], p.y],
                [s.z*r[2,0], s.z*r[2,1], s.z*r[2,2], p.z],
                [         0,          0,          0, 1],
            ])
            self.matrixUpdate = False
        return self.modelMatrix
    
    def moveTo(self, position=Vec3()):
        self.position     = position
        self.matrixUpdate = True
    
    def rotTo(self, rotation=Quaternion()):
        self.rotation     = rotation
        self.matrixUpdate = True
    
    def scaleTo(self, scale=Vec3(1,1,1)):
        self.scale        = scale
        self.matrixUpdate = True
    
    def setup(self, verts, ind, stride):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ind.nbytes, ind, GL_STATIC_DRAW)

        # Attribute 0: pos (3xf)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 
                              stride*np.dtype(np.float32).itemsize, 
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Attribute 1: Norm (3xf)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 
                              stride*np.dtype(np.float32).itemsize, 
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self, ind):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(ind), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)