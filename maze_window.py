"""
Create the window that show the maze and the pathfinder in action
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

import numpy as np
from copy import deepcopy
from math import floor
import pickle
import os

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
    color_map = plt.cm.get_cmap(BASE_COLOR_MAP, max_path)

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
        self.explore: bool = False

        # for best path animation
        self.animation_finished: bool = False

        # step of exploration
        self.step = 2

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
        Important function that will run animation of pathfinding (it is very dirty)
        :param i: frame
        :return: i
        """
        # instant explore
        # this condition if also called when Instant path ent path search are false (for a fastest exploration)
        if (self.explore and self.INSTANT_PATH) or (self.explore and not self.INSTANT_PATH and not self.PATH_SEARCH):
            # set exploration to false to prevent second call of the function
            self.explore = False

            # while the pathfinder did not find the arrival
            while True:
                # step by step exploration
                new_maze = next(self.solver)

                # if pathfiner find arrival
                if new_maze == True:
                    # stop while loop
                    break
                # add 1 to the exploration step
                self.step += 1

            # show the final maze with the exploration
            # create the color map
            c, n = colormap(self.step + 2)
            # get the final maze with the full exploration
            final_maze = next(self.solver)

            # set the maze final exploration in the gui
            self.mat.set_data(self.explore_enable(final_maze))
            self.mat.set_cmap(c)
            self.mat.set_norm(n)

            # show the best path
            if self.BEST_PATH and self.PATH_SEARCH:
                # create the generator that will return step by step the best path
                best_path = self.PATH_FINDER.show_path(final_maze,
                                                       self.arrival_point_x,
                                                       self.arrival_point_y,
                                                       self.step)
                # while the best path if not printed
                while True:
                    # step by step best path
                    new_maze = next(best_path)

                    # stop explore if maze == True,  when best path is fully printed
                    if new_maze == True:
                        break
                    else:

                        self.mat.set_data(self.explore_enable(new_maze))
                        plt.savefig(f"images/{self.step}.png", dpi=100)
            #  Instant path ent path search are false (for a fastest exploration)
            else:
                # stop explore
                self.explore = False
                # set variable to start best path visualisation
                self.animation_finished = True

                self.best_path = self.PATH_FINDER.show_path(final_maze,
                                                            self.arrival_point_x,
                                                            self.arrival_point_y,
                                                            self.step)

        # for animation during exploration
        elif self.explore and not self.INSTANT_PATH and self.PATH_SEARCH:
            # get exploration step by step
            new_maze = next(self.solver)

            # when the pathfinder find the arrival
            if new_maze == True:
                # stop explore
                self.explore = False
                # set variable to start best path visualisation
                self.animation_finished = True
                # get the final exploration maze
                full_explored_maze = next(self.solver)
                # init the best path visualisation
                self.best_path = self.PATH_FINDER.show_path(full_explored_maze,
                                                            self.arrival_point_x,
                                                            self.arrival_point_y,
                                                            self.step)
            # if exploration is not finished
            else:
                # show in the gui the advancement of the exploration
                c, n = colormap(self.step + 2)

                self.mat.set_data(self.explore_enable(new_maze))

                self.mat.set_cmap(c)
                self.mat.set_norm(n)
            # add on step
            self.step += 1

        # animation that show the best path after exploration
        elif not self.explore and not self.INSTANT_PATH and self.animation_finished:
            # get steps for best path visualisation
            best_path = next(self.best_path)
            # if it is the end of the best path visualisation
            if best_path == True:
                # stop animation
                self.animation_finished = False
            else:
                # else show advancement
                self.mat.set_data(self.explore_enable(best_path))

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
            self.solver = self.PATH_FINDER.solver(self.maze, self.starting_point_x, self.starting_point_y)
            # reset step
            self.step = 2

    def explore_enable(self, maze):
        """
        this function will remove every exploration color if the option is enable
        :param maze: a exploration maze
        :return: maze without color is the option is enable
        """
        if self.PATH_SEARCH:
            return maze
        else:
            no_exploration = np.array(maze)
            no_exploration[no_exploration > STARTING] = PATH
            return no_exploration


if __name__ == '__main__':
    """a = MazeWindow()
    a.main(20, 10, 25, True, True, True)"""

    # try open pickles conf
    if os.path.exists('conf.pkl'):
        # open the pickles configuration
        with open('conf.pkl', 'rb') as f:
            conf = pickle.load(f)
            f.close()

        os.remove("conf.pkl")
    else:
        conf = (25, 25, 25, False, True, True)

    M = MazeWindow()
    M.main(
        conf[0], conf[1], conf[2], conf[3], conf[4], conf[5]
    )
