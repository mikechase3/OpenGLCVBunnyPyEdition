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
        self.last_mouse_x = 0
        self.last_mouse_y = 0

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
        # print(f"New centroid: {new_centroid}")

    def apply_rotation_originToAxis(self, angle: float, axis: np.ndarray) -> None:
        """
        Applies a rotation to all vertices of the bunny model.

        Args:
            angle: The angle of rotation in radians.
            axis: A unit vector representing the axis of rotation.
                  This should be a numpy array of shape (3x1)

        Returns:
            None (modifies the object in-place)
        """
        c = np.cos(angle)
        s = np.sin(angle)
        t = 1.0 - c

        x, y, z = axis

        # Create the rotation matrix
        rotation_matrix = np.array([
            [t * x * x + c, t * x * y - z * s, t * x * z + y * s],
            [t * x * y + z * s, t * y * y + c, t * y * z - x * s],
            [t * x * z - y * s, t * y * z + x * s, t * z * z + c]
        ])

        # Apply the rotation matrix to all vertices
        for i in range(len(self.data.vertices)):
            self.data.vertices[i] = np.dot(rotation_matrix, self.data.vertices[i])

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


    def old_handle_mouse_motion(self, x, y):
        '''
        This function will be called whenever the mouse moves within the window while one or more mouse buttons are pressed.
        :return:
        '''
        dx = x - self.last_mouse_x
        dy = self.last_mouse_y - y  # Invert the y-coordinate

        if self.rotationMode:
            # Apply rotation based on mouse movement
            upVector = np.array[0, 1, 0]
            self.apply_rotation_originToAxis(dx / 100.0, upVector)
        else:
            # Apply transition based on mouse movement

            self.apply_translation(dx / 1000.0, dy / 1000.0, 0)
            # print("DEBUG: x:{} y: {}".format(dx, dy))

        self.last_mouse_x = x
        self.last_mouse_y = y

        glutPostRedisplay()

    def new_handle_mouse_motion(self, x: int, y: int):
        """
        Handles mouse motion events, updating the object's rotation or translation
        depending on the current mode.

        Args:
            x: The current X-coordinate of the mouse.
            y: The current Y-coordinate of the mouse.
        """
        dx = x - self.last_mouse_x
        dy = self.last_mouse_y - y

        if self.rotationMode:
            self.apply_rotation_from_mouse_delta(dx, dy)
        else:
            self.apply_translation_from_mouse_delta(dx, dy)

        self.last_mouse_x = x
        self.last_mouse_y = y
        glutPostRedisplay()

    def calculate_centroid(self):
        """Calculate the centroid of the model."""
        vertices = np.array(self.data.vertices)
        centroid = vertices.mean(axis=0)
        return centroid

    def create_rotation_matrix(self, axis: np.ndarray, angle: float) -> np.ndarray:
        """
        Creates a 4x4 rotation matrix around the given axis by the specified angle.

        Args:
            axis: A normalized 3D vector representing the axis of rotation.
            angle: The rotation angle in radians.

        Returns:
            A 4x4 NumPy array representing the rotation matrix.
        """
        # Implement using Rodrigues' rotation formula: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
        # ...
        return rotation_matrix

    def apply_rotation_from_mouse_delta(self, dx: float, dy: float):
        """
        Applies a rotation to the object based on the change in mouse coordinates.

        Args:
            dx: The change in mouse position along the X-axis.
            dy: The change in mouse position along the Y-axis.
        """
        if self.inArbitraryLineMode:
            # TODO: Handle rotation for arbitrary line mode.
            pass
        else:
            # Rotation around screen axes (simpler case for demonstration)
            axis = self.calculate_rotation_axis(dx, dy)  # Let's assume this gives a normalized axis vector
            angle = self.calculate_rotation_angle(dx, dy)

            # Create rotation matrix directly (quaternion conversion can be added later)
            rotation_matrix = self.create_rotation_matrix(axis, angle)

            # Apply transformation to vertices
            center = self.calculate_centroid()
            for i in range(len(self.data.vertices)):
                vertex_4d = np.append(self.data.vertices[i], 1)
                transformed_vertex = np.dot(rotation_matrix, vertex_4d)
                self.data.vertices[i] = transformed_vertex[:3] + center


        # 1. Calculate rotation axis and angle (details would depend on your desired behavior)
        axis = self.calculate_rotation_axis(dx, dy)
        angle = self.calculate_rotation_angle(dx, dy)

        # 2. Create a quaternion representing the rotation
        rotation_quaternion = self.create_quaternion_from_axis_angle(axis, angle)

        # 3. Apply the rotation to the vertices
        self.apply_quaternion_rotation(rotation_quaternion)

    def apply_translation_from_mouse_delta(self, dx: float, dy: float):
        """
        Applies a translation to the object based on the change in mouse coordinates.

        Args:
            dx: The change in mouse position along the X-axis.
            dy: The change in mouse position along the Y-axis.
        """
        # You might want to scale dx/dy by a factor for smoother movement
        self.apply_translation(dx, dy, 0)  # Assuming no Z-axis translation

    # ... Other helper functions like calculate_rotation_axis, calculate_rotation_angle, etc.


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glTranslatef(0.0, 0.0, -1.0)  # Move the triangle into the view
    gluLookAt(0.0, 1.0, 0.0,  # Camera position
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

    # Register the mouse motion callback function
    glutMotionFunc(bunbun.new_handle_mouse_motion)

    # Register the display callback function
    glutDisplayFunc(display)

    # Enter the GLUT event processing loop
    glutMainLoop()