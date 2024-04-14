import sys
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
        self.rotationMode: bool = True  # Set rotationMode to True by default

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
        for i in range(len(self.data.vertices)):
            vertex_4d = np.append(self.data.vertices[i], 1)  # 3D vertex => 4d by appending 1.
            translated_vertex = np.dot(translation_matrix, vertex_4d)  # Dot w/ translation matrix.
            self.data.vertices[i] = translated_vertex[:3]  # Update the vertex in-place

        # Calculate and print the new centroid
        new_centroid = self.calculate_centroid()
        print(f"New centroid: {new_centroid}")

    def apply_rotation(self, angle, axis):
        pass
        # Create rotation matrix using Rodrigues' rotation formula
        # Apply rotation matrix to all vertices

    def handle_key_press(self, key, x, y):
        '''
        In GLUT, you can register a keyboard callback function using glutKeyboardFunc. This function will be called whenever a key is pressed. The callback function should take two arguments: the key that was pressed and the x and y coordinates of the mouse at the time the key was pressed.  In your case, you want to toggle the inMeshVersion attribute of your Bunny object when the m or M key is pressed. You can do this by defining a method in your Bunny class that changes the value of inMeshVersion, and then passing this method to glutKeyboardFunc.
        :return:
        '''
        # print(f"Before glutGetModifiers in handle_key_press: {time.time()}")
        modifiers = glutGetModifiers()
        # print(f"After glutGetModifiers in handle_key_press: {time.time()}")

        if key == b'm' or key == b'M':
            self.inMeshVersion = not self.inMeshVersion
            glutPostRedisplay()  # Redraws.
        if key == b'0':
            self.inArbitraryLineMode = False
        if key == b'1':
            self.inArbitraryLineMode = True
        if key == b'\x1b':  # ASCII value for escape key (AI GENERATED)
            sys.exit(0)  # Exit the program on ESC key press

        if key == b'\x20':  # ASCII value for space bar
            # Reset the translation
            if self.rotationMode == False:
                self.rotationMode = True
            elif self.rotationMode == True:
                self.rotationMode = False

        # TODO: Fix Shift Not Working. (Use Space Instead For now)
        sys.stderr.write("Notice. def handle_key_press won't support shift; use space to toggle instead\n")
        if modifiers == GLUT_ACTIVE_SHIFT:
            print("ACTIVATE Translate Mode")
            self.rotationMode = False

    def handle_mouse_motion(self, x, y):
        '''
        This function will be called whenever the mouse moves within the window while one or more mouse buttons are pressed.
        :return:
        '''
        if self.rotationMode:
            # Apply rotation based on mouse movement
            self.apply_rotation(x / 100.0, (0, 1, 0))
        else:
            # Apply transition based on mouse movement
            self.apply_translation(x / 10000.0, y / 10000.0, 0)
        glutPostRedisplay()
    def handle_key_up(self, key, x, y):
        if key == GLUT_ACTIVE_SHIFT:
            self.rotationMode = True

    def calculate_centroid(self):
        """Calculate the centroid of the model."""
        vertices = np.array(self.data.vertices)
        centroid = vertices.mean(axis=0)
        return centroid



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
    gluPerspective(45, 800 / 600, 0.1, 100)  # fov, aspect ratio, near/far clipping plane

    # Switch back to model-view matrix mode
    glMatrixMode(GL_MODELVIEW)

    # Replace the current matrix with the identity matrix
    glLoadIdentity()

    # Create a Bunny object
    bunbun = Bunny("bunny_high.txt")  # Loads from obj

    # Register the keyboard callback function for key press events
    glutKeyboardFunc(bunbun.handle_key_press)

    # Register the keyboard callback function for key release events
    glutKeyboardUpFunc(bunbun.handle_key_up)

    # Register the mouse motion callback function
    glutMotionFunc(bunbun.handle_mouse_motion)

    # Register the display callback function
    glutDisplayFunc(display)

    # Enter the GLUT event processing loop
    glutMainLoop()