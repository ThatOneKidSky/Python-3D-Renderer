import numpy as np, pygame, math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from util import *
from system.Camera import Camera

# This stuff will be placed in a options.json file later
display   = (1000, 1000)
aspect    = display[0] / display[1]
mouseLock = False

mouseSensitivity = 0.005

# Temp function, used now to visualize the camera rotation
def drawSkybox(cameramatrix):
    verts = np.array([
        [-1,  1,  1], #0 Top left
        [ 1,  1,  1], #1 Top Right
        [ 1, -1,  1], #2 Bottom Right
        [-1, -1,  1], #3 Bottom Left
        [-1,  1, -1], #4 Top left
        [ 1,  1, -1], #5 Top Right
        [ 1, -1, -1], #6 Bottom Right
        [-1, -1, -1], #7 Bottom Left
    ],dtype=np.float32)

    edges = np.array([
        # Front
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        # Back
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 4],
        # Sides
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7],
    ],dtype=np.int32)

    tris = np.array([
        # Front
        [2, 1, 0],
        [0, 3, 2],
        # Back
        [4, 5, 6],
        [6, 7, 4],
        # Top
        [0, 1, 5],
        [5, 4, 0],
        # Bottom
        [2, 3, 7],
        [7, 6, 2],
        # Left
        [0, 4, 7],
        [7, 3, 0],
        # Right
        [6, 5, 1],
        [1, 2, 6],
    ],dtype=np.int32)

    glPushMatrix()

    glMultMatrixf(cameramatrix)

    glBegin(GL_TRIANGLES)
    for i, tri in enumerate(tris):
        for j, vert in enumerate(tri):
            glColor4fv([
                math.cos(math.floor(i/2)-math.pi/3*0), 
                math.cos(math.floor(i/2)-math.pi/3*2), 
                math.cos(math.floor(i/2)-math.pi/3*4), 1
                ])
            glVertex3fv(verts[vert])
    glEnd()

    glPopMatrix()

#region Init
# I always need to say bruv
def initGL():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, aspect, 0.1, 50.0)
    glTranslatef(0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

def initPygame():
    pygame.init()
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
#endregion

def toggleCursorLock():
    """Toggles if the window will hide and lock the cursor"""
    global mouseLock
    mouseLock = True if mouseLock == False else False

    pygame.mouse.set_visible(not mouseLock)
    pygame.event.set_grab(mouseLock)

def main():
    initPygame()
    initGL()

    camera = Camera(Vec3(), Quaternion())

    clock = pygame.time.Clock()
    running = True
    while running:
        # Events are fun
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    toggleCursorLock()
        
        # Clear buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Only allow cam rotation if 
        if mouseLock:
            mouseDx, mouseDy = pygame.mouse.get_rel()

            # Pitch -> Yaw -> Roll
            camera.rotate(-mouseDy*mouseSensitivity, -mouseDx*mouseSensitivity, 0)

        drawSkybox(camera.rotation.toMatrix())

        # Ill set up a delta frame system later
        pygame.display.flip()
        clock.tick(250)
    pygame.quit()



if __name__ == "__main__":
    main()