#include <stdio.h>
#include <stdlib.h>

/* 
A maze generator in C (there is no exporting function)
*/

void create_maze(int x_size, int y_size, int seed);

int is_finish(int x_size, int y_size, int maze[y_size][x_size]);

void print_maze(int x_size, int y_size, int maze[y_size][x_size]);

void save_maze(int x_size, int y_size, int maze[y_size * 2 + 1][x_size * 2 + 1]);

int main(int argc, char *argv[])
{
    create_maze(201, 201, s);
    return 0;
}

void create_maze(int x_size, int y_size, int seed)
{
    /*
    This function will create the full maze
    :param y_size: the height of the maze
    :param x_size: the length of the maze
    :param seed: the seed of the maze
    */

    // add seed to random
    srand(seed);

    // create the array that containe the maze
    int maze[(y_size * 2 + 1)][(x_size * 2 + 1)];

    // fill the maze of 2
    int value = 2;

    // for each line
    for (int y = 0; y < (y_size * 2 + 1); y++)
    {
        // for each column
        for (int x = 0; x < (x_size * 2 + 1); x++)
        {

            // put 1 for walls, n for path

            // to path value and add one for the next path value
            if (x % 2 == 1 && y % 2 == 1)
            {
                maze[y][x] = value;
                value++;
            }
            // put 1 for walls
            else
            {
                maze[y][x] = 1;
            }
        }
    }

    // n time that the program will run
    int tour = 0;

    // while the maze is not finished
    while (is_finish(y_size, x_size, maze) == 0)
    {

        int rep = 1; // optimization

        // if it is the first time that we change a value une the maze
        if (tour == 0)
        {
            tour++;
            rep = y_size * x_size;
        }

        for (int i = 0; i < rep; i++)
        {
            // while there is differente value in the maze

            // choose a random coordinate for breaking a wall
            int x = rand() % ((x_size - 1) * 2) + 2;
            int y;

            // if x is an odd number then the wall breaking is done on the top and the bottom
            // if x is an even number the breaking is done on the sides
            if (x % 2 == 1)
            {
                // breaking on the top/bottom

                y = rand() % (y_size - 1) * 2 + 2;

                // check if the wall has already been broken there if the wall has not yet been broken then continue labyrinth generation
                if (maze[y][x] == 1)
                {
                    // if the numbers in the two boxes to be broken are different
                    if (maze[y + 1][x] != maze[y - 1][x])
                    {
                        // then break the wall by putting the right value

                        // values ​​for change 1/2
                        int a_changer;
                        int changer_par;

                        if (rand() % 2 == 1)
                        {
                            a_changer = maze[y - 1][x];
                            changer_par = maze[y + 1][x];
                            maze[y][x] = changer_par;
                        }
                        else
                        {
                            a_changer = maze[y + 1][x];
                            changer_par = maze[y - 1][x];
                            maze[y][x] = changer_par;
                        }

                        // remplirer l'autre valeur par la bonne valeur
                        for (int y = 0; y < y_size; y++)
                        {
                            for (int x = 0; x < x_size; x++)
                            {
                                if (maze[y * 2 + 1][x * 2 + 1] == a_changer)
                                {
                                    maze[y * 2 + 1][x * 2 + 1] = changer_par;
                                }
                            }
                        }
                    }
                }
            }
            else
            {
                // breaking on the sides
                y = rand() % (y_size + 1) * 2 + 1;

                if (maze[y][x] == 1)
                {
                    // si les nombre dans les deux cases à casser sont différents
                    if (maze[y][x + 1] != maze[y][x - 1])
                    {
                        // if the numbers in the two boxes to be broken are different
                        maze[y][x] = maze[y][x + 1];

                        // values ​​for change
                        int a_changer;
                        int changer_par;

                        if (rand() % 2 == 1)
                        {
                            a_changer = maze[y][x - 1];
                            changer_par = maze[y][x + 1];
                            maze[y][x] = changer_par;
                        }
                        else
                        {
                            a_changer = maze[y][x + 1];
                            changer_par = maze[y][x - 1];
                            maze[y][x] = changer_par;
                        }

                        // fill the other value with the correct value
                        for (int y = 0; y < y_size; y++)
                        {
                            for (int x = 0; x < x_size; x++)
                            {
                                if (maze[y * 2 + 1][x * 2 + 1] == a_changer)
                                {
                                    maze[y * 2 + 1][x * 2 + 1] = changer_par;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    print_maze(y_size, x_size, maze);

    scanf("%d");
}

int is_finish(int x_size, int y_size, int maze[y_size * 2 + 1][x_size * 2 + 1])
{
    /*
    This function 1 returns if the game is over
    :param x_size, x_size : the size of the maze
    :param maze: the maze
    A maze if fully ended when there is only one value inside
	so we juste need to check if there is any différent value in the maze
    :return 1 if the generation is finished and 0 if it is not finished
    */

    int a_value = maze[1][1];

    for (int y = 0; y < y_size; y++)
    {
        for (int x = 0; x < x_size; x++)
        {
            // if a maze value is not equal to the base value, stop all
            if (maze[y * 2 + 1][x * 2 + 1] != a_value)
            {
                return 0;
            }
        }
    }
    // if all values ​​are the same then return that the maze is finished
    return 1;
}

void print_maze(int x_size, int y_size, int maze[y_size * 2 + 1][x_size * 2 + 1])
{
    /*
    this function is a debug function that print the maze in console 
    */
    for (int y = 0; y < (y_size * 2 + 1); y++)
    {
        printf("\n");
        // pour chaque colone
        for (int x = 0; x < (x_size * 2 + 1); x++)
        {

            if (maze[y][x] == 1)
            {
                printf(" O");
            }
            else
            {
                printf("  ");
            }
        }
    }
}

void save_maze(int x_size, int y_size, int maze[y_size * 2 + 1][x_size * 2 + 1])
{
    /*
    This function will save in data the maze
    :param x_size, x_size : the size of the maze
    :param maze: the maze
    */
}
