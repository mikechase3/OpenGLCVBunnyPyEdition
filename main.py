# This is a sample Python script.
import typing
from typing import Tuple
from Data import Data
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Data import Data


# Tutorials, not GLUT but not needed?
class Bunny:
    """
    Implements how we display the bunny model.
    """

    def __init__(self, filename: str):
        self.data = Data(filename)

    def render(self):
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.5, -0.5, 0.0)  # Define second vertex
        glVertex3f(0.0, 0.5, 0.0)  # Define third vertex
        glEnd()  # End rendering triangle primitives


    def translate(self, x: float, y: float, z: float):
        # Implement translation logic
        pass

    def rotate(self, angle: float, axis: typing.List[float]):
        # Implement rotation logic
        pass

    def scale(self, factor: float):
        # Implement scaling logic
        pass

    def handle_interaction(self):
        # Implement interaction handling logic
        pass

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    bunbun.render()
    glutSwapBuffers()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Bunny Model")
    glEnable(GL_DEPTH_TEST)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    bunbun = Bunny("bunny_high.txt")  # Loads it in.
    bunbun.render()

    glutDisplayFunc(display)
    glutMainLoop()