import unittest
from unittest.mock import patch
from Data import Data
import numpy as np
from main import Bunny

class TestData(unittest.TestCase):
    def test_add_vertex(self):
        data = Data()
        vertex = [1.0, 2.0, 3.0]
        data.add_vertex(vertex)
        self.assertEqual(data.vertices[0], vertex)

    def test_add_face(self):
        data = Data()
        face = [1, 2, 3]
        data.add_face(face)
        self.assertEqual(data.faces[0], face)

    @patch('builtins.input', return_value='1.0 2.0 3.0')
    def test_interactive_add_vertex(self, input):
        data = Data()
        data.interactive_add_vertex()
        self.assertEqual(data.vertices[0], [1.0, 2.0, 3.0])

    @patch('builtins.input', return_value='1 2 3')
    def test_interactive_add_face(self, input):
        data = Data()
        data.interactive_add_face()
        self.assertEqual(data.faces[0], [1, 2, 3])

    def test_apply_rotation_originToAxis(self):





if __name__ == '__main__':
    unittest.main()