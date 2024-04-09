# This is a sample Python script.
import typing
import numpy as np
from typing import Tuple
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Data import Data




class Bunny:
    """
    Implements how we display the bunny model.
    """

    def __init__(self, filename: str):
        self.data = Data(filename)

    def render(self):
        glBegin(GL_TRIANGLES)
        for face in self.data.iterFaces():
            for i in face:
                # Subtract one apparently b/c obj indices start at 1.
                vertex = self.data.vertices[i - 1]
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()


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
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -3.0)  # Move the triangle into the view
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

    glutDisplayFunc(display)
    glutMainLoop()