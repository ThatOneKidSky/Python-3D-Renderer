from util import *
from OpenGL.GL import *
import numpy as np
from object.Cube import Cube
import DEBUG

class Chunk:
    def __init__(self, size=32):
        self.size  = size
        self.tiles = np.zeros((size, size, size), dtype=np.uint8)
        
        self.VAO = None
        self.VBO = None
        self.EBO = None

        self.verts    = []
        self.indices = []
    
    def generate(self):
        #for x in range(self.size):
        #    for z in range(self.size):
        #        height = np.random.randint(4, 8)
        #        for y in range(height):
        #            self.tiles[x, y, z] = 1
        self.tiles[0, 0, :1] = 1
        if DEBUG.CHUNK.GENERATION:
            print(self.tiles)
        return
    
    def mesh(self):
        self.verts    = []
        self.indices = []
        indexOffset   = 0

        cubeVerts    = Cube.verticies
        cubeIndices = Cube.indices

        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if self.tiles[x,y,z] == 0:
                        continue

                    for i in range(Cube.stride):
                        self.verts.extend([
                            cubeVerts[i * Cube.stride + 0] + x,
                            cubeVerts[i * Cube.stride + 1] + y,
                            cubeVerts[i * Cube.stride + 2] + z,
                        ])
                    
                    for ind in cubeIndices:
                        self.indices.append(ind + indexOffset)

                    indexOffset += len(cubeVerts)
        
        if DEBUG.CHUNK.MESH:
            print(self.verts)

    def upload(self):
        self.clearVAO()
        
        vertArray  = np.array(self.verts, dtype=np.float32)
        indexArray = np.array(self.indices, dtype=np.uint32)

        self.VAO = GPU.upload(vertArray, indexArray, [3])
        if DEBUG.CHUNK.RENDER:
            print(vertArray)
    
    def clearVAO(self):
        if self.VAO is not None:
            glDeleteVertexArrays(1, [self.VAO])
    

    def render(self):
        if self.VAO is None:
            return
        
        GPU.draw(self.VAO, len(self.indices))