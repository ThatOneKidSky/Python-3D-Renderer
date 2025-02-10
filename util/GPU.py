import DEBUG
from OpenGL.GL import *
import numpy as np
import ctypes


class GPU:
    @staticmethod
    def upload(verts:np.ndarray, indices:np.ndarray, attribSizes:list):
        """
        Upload verticies and indicies to the GPU buffer.
        
        Parameters:
        - verts: Vertex array.
        - indicies: Indicies array.
        - attribSizes: Size of a vertex attribute (ie: [3, 4] for XYZ and RGBA)
        
        Returns VAO
        """

        if verts.size == 0 or indices.size == 0:
            raise ValueError("GPU.upload: Cannot upload empty array.")
        
        # Generate Buffers
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        # Bind Buffers (VAO)
        glBindVertexArray(VAO)

        # Bind Buffers (VBO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)

        # Bind Buffers (EBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Set Attributes
        stride = sum(attribSizes) * 4
        offset = 0

        for i, size in enumerate(attribSizes):
            glVertexAttribPointer(i, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
            glEnableVertexAttribArray(i)
            offset += size * 4

        # Unbind Buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        if DEBUG.GPU == True:
            print(f"Upload -> ({len(verts)//sum(attribSizes)} Verts, {len(indices)} Ind)")

        return VAO
    
    @staticmethod
    def loadShader(vertexPath, fragmentPath):
        # Load function since both shader types use the same code
        def load(path, stype):
            try:
                with open(f"shader/{path}.glsl", 'r') as f:
                    shader = glCreateShader(stype)
                    shaderSrc = f.read()

                    glShaderSource(shader, shaderSrc)
                    glCompileShader(shader)

                    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                        raise RuntimeError(glGetShaderInfoLog(shader))
                    return shader
            except FileNotFoundError:
                raise FileNotFoundError(f"{path} not found")
            except Exception as e:
                raise e

        # Load Vertex and Frament files
        vertexShader   = load(vertexPath, GL_VERTEX_SHADER)
        fragmentShader = load(fragmentPath, GL_FRAGMENT_SHADER)

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glLinkProgram(shaderProgram)

        if glGetProgramiv(shaderProgram, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(shaderProgram))
        
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

        return shaderProgram
    
    def draw(VAO, tris):
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, tris, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
