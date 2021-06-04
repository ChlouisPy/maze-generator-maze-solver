# maze-generator-maze-solver
This program will create a labyrinth and solve it by using Dijkstra's algorithm
You can change some parameters like the size of the maze or visual effects 

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/1.png?raw=true)
<br>

## How to use :
1. After launching the program the configuration window appears

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/3.png?raw=true)
<br>
- You can choose the size of the maze you want *(/!\ with more than 250 it takes few seconds to generate)*
- You can select a seed (default is random)
- You can modify some graphical parameters 
    * Instant pathfinding : If you want to see the progression of the pathfinder or not
    * Show best path : If you want to see the shortest path to the finish
    * Show path search : if you want to see how pathfinding works
- After configuration, you can press *Start Generate* to start the maze generation
<br>
  

2. After a new window will appear

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/4.png?raw=true)
<br>
   
- Left click will place the arrival point 
- Right click will place the starting point (by default it is in the upper left corner)

#### *Fun fact* :
- In [maze_window.py](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/maze_window.py) you can change *(line 23)* the colormap (default if plasma_r) there is a lot of customisation possibilities. *See [Matplolib colormaps documentation](https://matplotlib.org/stable/tutorials/colors/colormaps.html)*

## How it works :
#### - Maze generation :
To generate a maze, the program will create a matrix of (x*2 + 1) by (y * 2 + 1) it will then place, x * y point that do not touch each other and all have a different value. like this : 

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/8.png?raw=true)

*Black is 0 and white is different number per case*
To create the labyrinth, the program will break randomly some walls and put the value of one of the case to the whole space. like this : 

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/9.png?raw=true)

While there is more than two different value in the maze, the program continue to break random walls 
![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/11.png?raw=true)

#### - Maze solver :
*See [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)*


## Examples 
Some examples of maze solving you can do with this program :

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/5.gif?raw=true)
*Maze: 15x15 ; seed: 25 ; instant path: False ; best path: True ; path search: True ; cmap: plasma_r*
<br>

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/6.gif?raw=true)
*Maze: 50x50 ; seed: 42 ; instant path: False ; best path: True ; path search: True ; cmap: winter_r*
<br>

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/6.gif?raw=true)
*Maze: 25x25 ; seed: 42 ; instant path: False ; best path: True ; path search: False*
<br>

![alt text](https://github.com/ChlouisPy/maze-generator-maze-solver/blob/main/images/10.png?raw=true)
*Maze: 1000x1000 ; seed: 1000 ; instant path: True ; best path: False ; path search: True : cmap: summer_r*
*/!\ it takes more than 15 minutes to generate a 1000x1000 maze*
<br>

### Issue :
There is a strange issue with PyQt5 and Matplotlib, when you start a PyQt5 window, and you call (with a button for example) a Matplotlib window, animation and mouse click will not work.
To solve this issue, I call the Matplotlib window by using a command, and I pass arguments with a file (it is little bite dirty)

## Requirement :
- library     (*version that I use*)
- Numpy       (*1.18.0*)
- Matplotlib  (*3.3.3*)
- PyQt5       (*5.15.4*)

## Credit :
- [ChlouisPy](https://github.com/ChlouisPy/)

