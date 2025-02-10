import numpy as np, pygame, math, DEBUG, SETTINGS, random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from objects import *
from util import *
from system import *

mouseLock = False
mouseSensitivity = 0.005

def toggleCursorLock():
    """Toggles if the window will hide and lock the cursor"""
    global mouseLock
    mouseLock = True if mouseLock == False else False

    pygame.mouse.set_visible(not mouseLock)
    pygame.event.set_grab(mouseLock)

def main():
    camera = Camera(Vec3(0, 60, 0), Quaternion())
    window = Window(camera=camera,vertex='depthnormal/vertex',fragment='depthnormal/fragment')

    toRender = []
    for x in range(50):
        for y in range(50):
            toRender.append(Cube(Vec3(x-5,random.randint(0,50),y-5), 
                            Quaternion.fromEuler(0,0,0),
                            Vec3(random.randint(1,10),random.randint(1,10),random.randint(1,10))
                            ))
    
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_DEPTH_TEST)

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
        CAMERA_SPEED = 0.5
        if mouseLock:
            mouseDx, mouseDy = pygame.mouse.get_rel()
            camera.rotate(-mouseDy*mouseSensitivity, -mouseDx*mouseSensitivity, 0)
            keys = pygame.key.get_pressed()  # Get the state of all keys
            if keys[pygame.K_w]:
                camera.position += camera.forward * CAMERA_SPEED  # Move forward
            if keys[pygame.K_s]:
                camera.position -= camera.forward * CAMERA_SPEED  # Move backward
            if keys[pygame.K_a]:
                camera.position -= camera.right * CAMERA_SPEED  # Move left
            if keys[pygame.K_d]:
                camera.position += camera.right * CAMERA_SPEED  # Move right
            if keys[pygame.K_SPACE]:
                camera.position += camera.up * CAMERA_SPEED  # Move left
            if keys[pygame.K_LSHIFT]:
                camera.position -= camera.up * CAMERA_SPEED  # Move right
            if keys[pygame.K_e]:
                camera.rotate(Quaternion.fromEuler(0, 0, -0.01))
            if keys[pygame.K_q]:
                camera.rotate(Quaternion.fromEuler(0, 0, 0.01))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(window.shader)
        
        # These stay the same between frames
        vMatrix = camera.viewMatrix
        pMatrix = window.projectionMatrix
        
        glUniformMatrix4fv(glGetUniformLocation(window.shader, "view"),       1, GL_TRUE, vMatrix)
        glUniformMatrix4fv(glGetUniformLocation(window.shader, "projection"), 1, GL_TRUE, pMatrix)

        # Then render each object
        for model in toRender:
            try:
                mMatrix = model.getModelMatrix()

                glUniformMatrix4fv(glGetUniformLocation(window.shader, "model"), 1, GL_TRUE, mMatrix)

                model.render()
            except Exception as e:
                print(e)

        #print(window.activeCamera.up)

        pygame.display.flip()
        clock.tick(60)
        fps = clock.get_fps()
        pygame.display.set_caption(str(fps))
    pygame.quit()

if __name__ == "__main__":
    main()