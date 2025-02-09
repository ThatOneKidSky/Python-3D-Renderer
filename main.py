import numpy as np, pygame, math, SETTINGS
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from util import *
from system.Camera import Camera
from system.Chunk import *

mouseLock = False
mouseSensitivity = 0.005

shader = None

#region Init
# I always need to say bruv
def initGL():
    global shader
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, SETTINGS.SCREEN.ASPECT, 0.1, 50.0)
    glTranslatef(0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)


    shader = GPU.loadShader("shader/vertex.glsl", "shader/fragment.glsl")

def initPygame():
    pygame.init()
    pygame.display.set_mode((SETTINGS.SCREEN.WIDTH, SETTINGS.SCREEN.HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
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
    chunk = Chunk()
    chunk.generate()
    chunk.mesh()
    chunk.upload()

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

        # Only allow cam rotation if in screen
        if mouseLock:
            mouseDx, mouseDy = pygame.mouse.get_rel()

            # Pitch -> Yaw -> Roll
            #camera.rotate(-mouseDy*mouseSensitivity, -mouseDx*mouseSensitivity, 0)
        camera.rotate(0, 0, 0.01)
        
        # Clear screen/buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set active shader
        glUseProgram(shader)

        # Get "in"s for shader
        viewLoc  = glGetUniformLocation(shader, "view")
        projLoc  = glGetUniformLocation(shader, "proj")
        modelLoc = glGetUniformLocation(shader, "model")

        # Matrices
        vm = camera.viewMatrix
        pm = camera.projectionMatrix
        mm = np.eye(4, dtype=np.float32)

        # Pass in to shaders
        glUniformMatrix4fv(viewLoc,  1, GL_TRUE, vm)
        glUniformMatrix4fv(projLoc,  1, GL_TRUE, pm)
        glUniformMatrix4fv(modelLoc, 1, GL_TRUE, mm)

        glViewport(0, 0, SETTINGS.SCREEN.WIDTH, SETTINGS.SCREEN.HEIGHT)

        # Render
        chunk.render()

        # Reset for next frame
        glUseProgram(0)

        if DEBUG.CAMERA.DIRECTION:
            print(camera.up)

        pygame.display.flip()
        clock.tick(250)
    pygame.quit()



if __name__ == "__main__":
    main()