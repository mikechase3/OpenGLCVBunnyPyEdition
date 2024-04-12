import typing
import numpy as np
import time
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
        self.inMeshVersion: bool = False
        self.inArbitraryLineMode: bool = False
        self.inTranslateMode: bool = False

    def render(self):
        if self.inMeshVersion:
            glBegin(GL_LINE_LOOP)
            for face in self.data.iterFaces():
                for i in face:
                    # Subtract one apparently b/c obj indices start at 1.
                    vertex = self.data.vertices[i - 1]
                    glColor3f(1.0, 0.0, 0.0)
                    glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()
        elif not self.inMeshVersion:
            glBegin(GL_TRIANGLES)
            for face in self.data.iterFaces():
                for i in face:
                    # Subtract one apparently b/c obj indices start at 1.
                    vertex = self.data.vertices[i - 1]
                    glColor3f(1.0, 0.0, 0.0)
                    glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()

    def create_translation_matrix(self, x: float, y: float, z: float) -> np.array:
        """Creates a 4x4 translation matrix"""
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    def apply_translation(self, x: float, y: float, z: float):
        """Apply a translation matrix to all vertices."""
        # Create a translation matrix
        translation_matrix = self.create_translation_matrix(x, y, z)

        # Apply the translation matrix to all vertices
        translated_vertices = []
        for vertex in self.data.vertices:
            vertex_4d = np.append(vertex, 1)  # 3D vertex => 4d by appending 1.
            translated_vertex = np.dot(translation_matrix, vertex_4d)  # Dot w/ translation matrix.
            translated_vertices.append(translated_vertex)
        self.data.vertices = translated_vertices  # OVERWRITES original list.
    def rotate(self, angle, axis):
        pass
        # Create rotation matrix using Rodrigues' rotation formula
        # Apply rotation matrix to all vertices


    def handle_key_press(self, key, x, y):
        '''
        In GLUT, you can register a keyboard callback function using glutKeyboardFunc. This function will be called whenever a key is pressed. The callback function should take two arguments: the key that was pressed and the x and y coordinates of the mouse at the time the key was pressed.  In your case, you want to toggle the inMeshVersion attribute of your Bunny object when the m or M key is pressed. You can do this by defining a method in your Bunny class that changes the value of inMeshVersion, and then passing this method to glutKeyboardFunc.
        :return:
        '''
        print(f"Before glutGetModifiers in handle_key_press: {time.time()}")
        modifiers = glutGetModifiers()
        print(f"After glutGetModifiers in handle_key_press: {time.time()}")

        if key == b'm' or key == b'M':
            self.inMeshVersion = not self.inMeshVersion
            glutPostRedisplay()  # Redraws.
        if key == b'0':
            self.inArbitraryLineMode = False
        if key == b'1':
            self.inArbitraryLineMode = True

        if modifiers == GLUT_ACTIVE_SHIFT:
            print("ACTIVATE Translate Mode")
        else:
            self.inTranslateMode = False

    def handle_mouse_motion(self, x, y):
        '''
        This function will be called whenever the mouse moves within the window while one or more mouse buttons are pressed.
        :return:
        '''
        print(f"Before glutGetModifiers in handle_mouse_motion: {time.time()}")
        modifiers = glutGetModifiers()
        print(f"After glutGetModifiers in handle_mouse_motion: {time.time()}")
        # rest of your code...
        if modifiers == GLUT_ACTIVE_SHIFT:
            self.inTranslateMode = True
            # print("ACTIVATE Translate Mode")
        else:
            self.inTranslateMode = False
            # print("Deactivated Translate Mode")

        if self.inTranslateMode:
            # Apply translation based on mouse movement (scaled down by 100x)
            self.apply_translation(x / 10.0, y / 10.0, 0)
            glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glTranslatef(0.0, 0.0, -1.0)  # Move the triangle into the view
    gluLookAt(0.0, 1.0, 1.0,  # Camera position
              0.0, 0.0, 0.0,  # Look at origin
              0.0, 1.0, 0.0)  # Up vector is Y-axis

    bunbun.render()
    glutSwapBuffers()



if __name__ == "__main__":
    # Initialize the GLUT library
    glutInit()

    # Set the initial display mode. GLUT_DOUBLE enables double buffering,
    # GLUT_RGB sets the color mode to RGB, and GLUT_DEPTH enables the depth buffer.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    # Set the initial window size
    glutInitWindowSize(800, 600)

    # Create a window with a given title
    glutCreateWindow(b"Bunny Model")

    # Enable depth testing. This is necessary for correct rendering of 3D objects,
    # as it allows OpenGL to know which objects are in front of others.
    glEnable(GL_DEPTH_TEST)

    # Set the clear color to black
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Set the current matrix mode to projection to set up the camera lens
    glMatrixMode(GL_PROJECTION)

    # Replace the current matrix with the identity matrix
    glLoadIdentity()

    # Set up a perspective projection matrix
    gluPerspective(45, 800/600, 0.1, 100)  # fov, aspect ratio, near/far clipping plane

    # Switch back to model-view matrix mode
    glMatrixMode(GL_MODELVIEW)

    # Replace the current matrix with the identity matrix
    glLoadIdentity()

    # Create a Bunny object
    bunbun = Bunny("bunny_high.txt")  # Loads from obj

    # Register the keyboard callback function
    glutKeyboardFunc(bunbun.handle_key_press)

    # Register the mouse motion callback function
    glutMotionFunc(bunbun.handle_mouse_motion)

    # Register the display callback function
    glutDisplayFunc(display)

    # Enter the GLUT event processing loop
    glutMainLoop()