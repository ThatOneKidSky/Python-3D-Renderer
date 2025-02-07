<div align="center">
  <h1>Sky's 3D Python Engine</h1>
  <p>A horrible way to make a graphics engine!
 </p>
</div>
<br>

A simple 3D engine, written in Python, that uses OpenGL. On the user side there is, camera rotation... Amazing.

# Features
Camera System: Control the camera's orientation (pitch, yaw, roll).
Skybox: A very bare bones skybox that is less of a skybox as apposed to as cube that just so happens to encapsulate the camera.
OpenGL: Using OpenGL for rendering, because pygame just isnt fast enough for what I have planned.
User Input: Mouse input for controlling camera rotation.

# Requirements:
- Python (Im using 3.11.5)
- PyOpenGL
- pygame
- NumPy

Everything else is built in house (or stolen from my other projects, sucks to be past me)

# Controls
_Mouse_: Move the mouse to rotate the camera.
Escape: Exit the application.

# Camera
The camera is basic for now, no projection or other such fun stuff. The camera has pitch and yaw, both relative to itself (ie: up is not always y+). No controls yet for roll, but Ive got plans!

# Roadmap
- Add camera movement
- Add objects in the world
- Add the ability to load images and display them on faces
