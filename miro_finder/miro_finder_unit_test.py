# -*- coding: utf8 -*-

import unittest
import os
import urllib.request
import pickle
from datetime import datetime


import miro_finder as mf


class MyMifoFinder(unittest.TestCase):
    def test_get_maze_answer(self):
        maze = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1},
                (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0},
                (5, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
                (3, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
                (2, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 4): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0},
                (4, 5): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
        solution = [(5, 5),  (5, 4), (4, 4), (4, 3), (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (2, 5), (2, 4), (2, 3), (2, 2), (1, 2), (1, 1)]
        self.assertEqual(
            solution, mf.get_maze_answer(maze))
        
        maze = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1},
                (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0},
                (5, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
                (3, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
                (2, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 4): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0},
                (4, 5): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
        solution = [(5, 5),  (5, 4), (4, 4), (4, 3), (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (2, 5), (2, 4), (2, 3), (2, 2), (1, 2), (1, 1)]
        self.assertEqual(
            solution, mf.get_maze_answer(maze))

        maze = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1},
                (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0},
                (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0},
                (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0},
                (2, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1},
                (3, 2): {'E': 1, 'W': 1, 'N': 1, 'S': 0},
                (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1},
                (2, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1},
                (3, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
        solution = [(3, 3), (3, 2), (2, 2), (2, 1), (1, 1)]
        self.assertEqual(
            solution, mf.get_maze_answer(maze))