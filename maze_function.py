"""
All function for maze generation and maze solving
Create labyrinths (necessarily possible to solve) and uses Dijkstra's algorithm to solve it
"""

import numpy as np
import os
from ctypes import *
import time
import random
from copy import deepcopy

# maze value
PATHFINDING: int = -2
ARRIVAL: int = -1
WALL: int = 0
PATH: int = 1
STARTING: int = 2


class Maze:
    """
    class which contains all the functions concerning the generation of a maze

    information about maze :
    0 = wall
    1 = path
    -1 = arrival
    """

    def __init__(self):
        # load go library
        localisation = os.path.abspath("maze.so")
        self.lib = cdll.LoadLibrary(localisation)
        self.lib.labyrinthe.argtypes = [c_longlong, c_longlong, c_longlong]

        # pre create variable
        self.maze = []

    @staticmethod
    def load_maze(file="data") -> [[int]]:
        """
        load a maze from a file (generated before)
        :param file: name of the file
        :return: The maze as a list of list
        """
        return np.loadtxt(file).tolist()

    def generate(self, length, height, seed=random.randint(1, 2147483647)) -> None:
        """
        :param length: the length of the maze
        :param height: the height of the maze
        :param seed: the seed for the maze
        :return: None
        """
        # time at the start of the creation of the maze
        t = time.time()

        # generate the maze
        self.lib.labyrinthe(length, height, seed)

        # print time at the end of the creation of the maze
        print(f"Labyrinth generated in {round(time.time() - t, 1)} seconds")


class PathFinder:
    """
    This class contain every function for the maze solver
    uses Dijkstra's algorithm to solve the maze
    """

    def solver(self, base_maze, depart_x, depart_y):
        """
        This generators will return each step of the path finding search
        :return: each step in maze search
        """
        # copy of the maze
        maze = deepcopy(base_maze)

        last_x: list = [depart_x]
        last_y: list = [depart_y]

        is_finished = False

        while not is_finished:

            future_x, future_y = [], []

            # for each coordinate to explore

            for i, (x, y) in enumerate(zip(last_x, last_y)):

                # value of the case
                value_case = int(maze[y][x])

                # check each of the 4 possible move, check if it can explore and check if it is the arival

                # top
                # check if it is the arrival
                top_case_value = maze[y + 1][x]
                if top_case_value == ARRIVAL:
                    is_finished = True
                    yield True
                # check if we can explore
                # if it is a path       or if the value is superior
                elif top_case_value == PATH or (top_case_value > value_case and top_case_value != WALL):
                    maze[y + 1][x] = value_case + 1
                    # add value of this coordinate for future
                    future_y.append(y + 1), future_x.append(x)

                # bottom
                bottom_case_value = maze[y - 1][x]
                if bottom_case_value == ARRIVAL:
                    is_finished = True
                    yield True

                elif bottom_case_value == PATH or (bottom_case_value > value_case and bottom_case_value != WALL):
                    maze[y - 1][x] = value_case + 1
                    future_y.append(y - 1), future_x.append(x)

                # left
                left_case_value = maze[y][x - 1]
                if left_case_value == ARRIVAL:
                    is_finished = True
                    yield True

                elif left_case_value == PATH or (left_case_value > value_case and left_case_value != WALL):
                    maze[y][x - 1] = value_case + 1
                    future_y.append(y), future_x.append(x - 1)

                # right
                right_case_value = maze[y][x + 1]
                if right_case_value == ARRIVAL:
                    is_finished = True
                    yield True

                elif right_case_value == PATH or (right_case_value > value_case and right_case_value != WALL):
                    maze[y][x + 1] = value_case + 1
                    future_y.append(y), future_x.append(x + 1)

            # set future coordinate for next round of exploration
            last_y = deepcopy(future_y)
            last_x = deepcopy(future_x)

            # return maze with advancement of one case
            yield maze



if __name__ == '__main__':

    m = Maze()
    m.generate(5, 5, 5)
    b = m.load_maze()
    # set arrival
    b[-2][-2] = ARRIVAL
    b[1][1] = STARTING
    #
    p = PathFinder()
    g = p.solver(b, 1, 1, -2, -2)
    while True:
        print(np.array(next(g)))
        print("=================================")
        time.sleep(1)
