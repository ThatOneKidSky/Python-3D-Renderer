import SETTINGS, math, numpy as np, pygame
from util import *
from .Camera import Camera
from OpenGL.GL import *

class Window:
    def __init__(self, resolution=Vec2(SETTINGS.SCREEN.WIDTH, SETTINGS.SCREEN.HEIGHT), camera=Camera(Vec3(), Quaternion()), vertex='default/vertex', fragment='default/fragment'):
        self.resolution   = resolution
        self.aspectRatio  = resolution.x/resolution.y
        self.activeCamera = camera

        # Projection matrix shouldnt really ever update unless fov or resolution is changed
        # But for now it wont, later it will
        self.projectionMatrix = self.getProjectionMatrix()

        # Init Pygame (ill add an update display later)
        pygame.init()
        pygame.display.set_mode(
            (SETTINGS.SCREEN.WIDTH, SETTINGS.SCREEN.HEIGHT),
            pygame.DOUBLEBUF | pygame.OPENGL)
        
        # Init GL, not much needed
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.shader = GPU.loadShader(vertex, fragment)
        
    def getProjectionMatrix(self):
        fovRad = math.radians(self.activeCamera.FOV)
        NEAR   = self.activeCamera.NEAR
        FAR    = self.activeCamera.FAR

        f   = 1 / math.tan(fovRad/2)
        fa  = f / self.aspectRatio
        fp1 = (FAR + NEAR) / (NEAR - FAR)
        fp2 = (2 * FAR * NEAR) / (NEAR - FAR)
        return np.array([
            [fa, 0,    0,   0],
            [ 0, f,    0,   0],
            [ 0, 0,  fp1, fp2],
            [ 0, 0,   -1,   0],
        ], dtype=np.float32)