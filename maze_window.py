"""
Create the window that show the maze and the pathfinder in action
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

import numpy as np
from copy import deepcopy
from math import floor
import time

from maze_function import Maze
from maze_function import PathFinder
from maze_function import PATHFINDING, STARTING, ARRIVAL, WALL, PATH

# disable menu bar in matplotlib window
# matplotlib.rcParams['toolbar'] = 'None'

# color configuration
PAD: float = 0.5
BASE_COLOR_MAP: str = "plasma_r"

# create color map for specific element
PATHFINDING_COLOR: tuple = (0, 1.0, 0.0)  # -2 is for path finder
STARTING_COLOR: tuple = (1.0, 0.0, 0.0)  # -1 is for starting point
WALL_COLOR: tuple = (1.0, 1.0, 1.0)  # 0 is for wall
PATH_COLOR: tuple = (0.0, 0.0, 0.0)  # 1 is for path
ARRIVAL_COLOR: tuple = (0.0, 0.0, 1.0)  # 2 is for arrival

# color map as array
FULL_MAP: list = [PATHFINDING_COLOR, STARTING_COLOR, PATH_COLOR, WALL_COLOR, ARRIVAL_COLOR]
# color for value
FULL_BOUNDS = (np.array([-3, -2, -1, 0, 1, 2], dtype=np.float) + PAD).tolist()


def colormap(max_path: int) -> (matplotlib.colors.ListedColormap, matplotlib.colors.BoundaryNorm):
    """
    This function will return the colormap for the matplotlib window
    :param max_path : The value for the maximum path advancement min 2 and max +Inf
    :return: color_map and norm
    """
    # get maplotlib base colormap
    color_map = plt.cm.get_cmap("plasma_r", max_path)

    # create map
    maps = deepcopy(FULL_MAP)
    bound = deepcopy(FULL_BOUNDS)

    # create each color for each value
    for i in range(2, max_path):
        maps.append(color_map(i))
        bound.append(i + PAD)

    # create the color map
    color_map = matplotlib.colors.ListedColormap(maps)
    norm = matplotlib.colors.BoundaryNorm(bound, color_map.N)

    return color_map, norm


class MazeWindow:
    """
    This class contains all the functions for the maze window

    maze array : 0 = wall and 1 = path
    """

    def __init__(self):
        # create class for pathfinder and maze_generator
        self.MAZE = Maze()
        self.PATH_FINDER = PathFinder()

        # create main matplotlib window
        self.fig, self.ax = plt.subplots(1, 1)
        self.fig.set_size_inches(9, 9)

        # create the variable that will contain the maze
        self.maze: np.array = np.array([])

        # starting point
        self.starting_point_x: int = 1
        self.starting_point_y: int = 1

        # arrival point
        self.arrival_point_x: int = -2
        self.arrival_point_y: int = -2

        # base config
        self.INSTANT_PATH: bool = False
        self.BEST_PATH: bool = True
        self.PATH_SEARCH: bool = True

        # other

        # if you can explore
        self.explore = False

    def main(self,
             maze_size_x: int,
             maze_size_y: int,
             maze_seed: int,
             instant_path: bool,
             best_path: bool,
             path_search: bool) -> None:
        """
        generate the maze and start the main window
        :param maze_size_x: the length of the maze
        :param maze_size_y: the height of the maze
        :param maze_seed: the seed for the maze

        :param instant_path: if you want animation of searching
        :param best_path: if you want two see the best path
        :param path_search: if you want see the search in color
        :return: None
        """

        # set the new configuration
        self.INSTANT_PATH = instant_path
        self.BEST_PATH = best_path
        self.PATH_SEARCH = path_search

        # create the main maze
        self.MAZE.generate(maze_size_x, maze_size_y, maze_seed)

        # get the maze
        self.maze = self.MAZE.load_maze()

        # set starting point on the board
        self.maze[self.starting_point_y][self.starting_point_x] = STARTING

        # get base colormap
        color_map, norm = colormap(2)

        # plot maze
        self.mat = self.ax.matshow(self.maze, cmap=color_map, norm=norm)

        # disable boarder on the matplotlib window
        plt.subplots_adjust(bottom=0, left=0, top=1, right=1)

        # create a animation for the window
        ani = animation.FuncAnimation(self.fig, self.animation_function, interval=1)

        # add click detection
        self.fig.canvas.mpl_connect('button_press_event', self.click_window)

        # plot window
        plt.show()

    def animation_function(self, i) -> int:
        """
        Important function that will run animation of pathfinding
        :param i: frame
        :return: i
        """
        # instant explore
        if self.explore and self.INSTANT_PATH:

            self.explore = False

            while True:
                # step by step explortion
                new_maze = next(self.G)

                # stop explore if maze == True
                if new_maze == True:
                    break
                self.step += 1

            # show the final maze
            c, n = colormap(self.step + 2)
            # show the final maze with path search
            if self.PATH_SEARCH:
                self.mat.set_data(next(self.G))
                self.mat.set_cmap(c)
                self.mat.set_norm(n)
            # show the final maze without path search
            else:
                self.mat.set_data(self.maze)

        # for animation during exploration
        elif self.explore and not self.INSTANT_PATH:

            new_maze = next(self.G)

            if new_maze == True:
                self.explore = False
            else:

                c, n = colormap(self.step + 2)

                self.mat.set_data(new_maze)
                self.mat.set_cmap(c)
                self.mat.set_norm(n)

            self.step += 1

        return i

    def click_window(self, event) -> None:
        """
        This function is for mouse click
        if left click is pressed, it change the arrival point
        if right click is pressed, it change the starting point
        :param event: information about the click
        :return: None
        """

        # get coordinate of the click and button pressed (1 = left and 3 = right)
        x, y, button = floor(event.xdata + 0.5), floor(event.ydata + 0.5), int(event.button)

        # check if there is no wall at the new coordinate
        if self.maze[y][x] != WALL:

            # for left click, set arrival point
            if button == 1:
                # delete last depart point
                self.maze[self.arrival_point_y][self.arrival_point_x] = PATH

                # set new coordinate
                self.arrival_point_x = x
                self.arrival_point_y = y

                # set new arrival point
                self.maze[self.arrival_point_y][self.arrival_point_x] = ARRIVAL

            # for right click, set starting point
            elif button == 3:
                # delete last depart point
                self.maze[self.starting_point_y][self.starting_point_x] = PATH

                # set new coordinate
                self.starting_point_x = x
                self.starting_point_y = y

                # set new arrival point
                self.maze[self.starting_point_y][self.starting_point_x] = STARTING

            self.mat.set_data(self.maze)
            # self.mat.set_cmap()
            # self.mat.set_norm()
            # now we can explore because we set the arrival and starting points
            self.explore = True

            # create the pathfinder
            self.G = self.PATH_FINDER.solver(self.maze, self.starting_point_x, self.starting_point_y)
            #
            self.step = 2


if __name__ == '__main__':
    a = MazeWindow()
    a.main(25, 25, 25, False, True, True)
