from typing import List


class Data:
    """
    Provides a way to interface to represent vertex data.
    Can be used by other libraries easily so i can use it between OpenCV/GL/NumPy if necessary.
    """
    def __init__(self, filename=None):
        self.vertices = []
        self.faces = []
        if filename:
            # Read the file
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith('v'):
                        try:
                            vertex = [float(x) for x in line.strip().split()[1:]]
                            if len(vertex) != 3:
                                raise ValueError("A vertex must have three coordinates.")
                            self.vertices.append(vertex)
                        except ValueError as e:
                            print(f"Invalid vertex data: {e}")
                    if line.startswith('f'):
                        try:
                            face = [int(x) for x in line.strip().split()[1:]]
                            if len(face) != 3:
                                raise ValueError("A face must have three indices.")
                            self.faces.append(face)
                        except ValueError as e:
                            print(f"Invalid face data: {e}")

    def __repr__(self):
        s = []
        s.append("This is a poor representation but it'll work. Here's the first 5 vertices & faces listed.")
        for i in range(5):
            s.append(self.vertices[i])
            s.append(self.faces[i])
        s.append("... see debugger for more")
        return str(s)

    def __iter__(self):
        return iter(self.vertices + self.faces)

    # Getters/Adders for our data.
    # It's also an interactive interface for debugging.
    def add_vertex(self, vertex):
        if len(vertex) != 3:
            raise ValueError("A vertex must have three coordinates.")
        self.vertices.append(vertex)

    def add_face(self, face):
        if len(face) != 3:
            raise ValueError("A face must have three indices.")
        self.faces.append(face)

    def interactive_add_vertex(self):
        vertex = input("Enter the coordinates for the vertex, separated by spaces: ").split()
        try:
            vertex = [float(x) for x in vertex]
            if len(vertex) != 3:
                raise ValueError("A vertex must have three coordinates.")
            self.add_vertex(vertex)
        except ValueError as e:
            print(f"Invalid input: {e}")

    def interactive_add_face(self):
        face = input("Enter the indices for the face, separated by spaces: ").split()
        try:
            face = [int(x) for x in face]
            if len(face) != 3:
                raise ValueError("A face must have three indices.")
            self.add_face(face)
        except ValueError as e:
            print(f"Invalid input: {e}")


