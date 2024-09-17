"""
Maze Generator

This script generates a 20x20 random maze with a guaranteed solution using
the Recursive Backtracking algorithm. The maze has walls on all edges except
for the entrance at the top-left corner (marked 'S') and the exit at the
bottom-right corner (marked 'E'). The maze only allows movement in four main
directions: North, South, East, and West.

ASCII Representation:
- '#' represents walls
- 'S' represents the start
- 'E' represents the exit
- ' ' (space) represents empty corridors
"""

import random

MAZE_WIDTH = 20
MAZE_HEIGHT = 20

WALL = '#'
START = 'S'
EXIT = 'E'
PATH = ' '  # Empty space represents corridors


def generate_maze(width, height):
    """
    Generates a random maze using the Recursive Backtracking algorithm.

    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.

    Returns:
        list: A 2D list representing the maze.
    """
    # Initialize the maze with walls
    maze = [[WALL for _ in range(width)] for _ in range(height)]

    # Create a grid of cells, where each cell is surrounded by walls
    # The actual maze paths will be carved between these cells
    # Adjust dimensions to ensure walls around the maze
    maze_cells_width = (width - 1) // 2
    maze_cells_height = (height - 1) // 2

    # Starting position (entrance)
    start_x, start_y = 0, 0
    maze[start_y][start_x] = START

    # Adjust exit position (ensure it's on the edge)
    exit_x, exit_y = width - 1, height - 1

    # Recursive Backtracking using stack
    def carve_passages_from(cx, cy):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # N, S, W, E
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == WALL:
                wall_x, wall_y = cx + dx // 2, cy + dy // 2
                maze[wall_y][wall_x] = PATH
                maze[ny][nx] = PATH
                carve_passages_from(nx, ny)

    # Start carving from cell (1,1)
    maze[1][1] = PATH
    carve_passages_from(1, 1)

    # Set the exit
    maze[exit_y][exit_x] = EXIT

    # Ensure walls around the maze except entrance and exit
    for x in range(width):
        if (x, 0) != (start_x, start_y):
            maze[0][x] = WALL
        if (x, height - 1) != (exit_x, exit_y):
            maze[height - 1][x] = WALL

    for y in range(height):
        maze[y][0] = WALL if (0, y) != (start_x, start_y) else maze[y][0]
        maze[y][width - 1] = WALL if (width - 1, y) != (exit_x, exit_y) else maze[y][width - 1]

    return maze


def print_maze(maze):
    """
    Prints the maze using ASCII graphics.

    Args:
        maze (list): The maze to print.
    """
    for row in maze:
        print(''.join(row))


def main():
    """
    Main function to generate and print the maze.
    """
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    print_maze(maze)


if __name__ == '__main__':
    main()
