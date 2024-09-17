import random
from typing import List, Tuple

# Constants
MAZE_SIZE = 10  # Defines the number of cells in one dimension
GRID_SIZE = 2 * MAZE_SIZE + 1  # Actual grid size including walls
WALL = '#'
PATH = ' '
START = 'S'
EXIT = 'E'

def initialize_maze() -> List[List[str]]:
    """
    Initializes the maze grid with walls.

    Returns:
        List[List[str]]: A 2D grid representing the maze initialized with walls.
    """
    return [[WALL for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def print_maze(maze: List[List[str]]):
    """
    Prints the maze in ASCII format.

    Args:
        maze (List[List[str]]): The 2D grid representing the maze.
    """
    for row in maze:
        print(''.join(row))

def get_neighbors(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Retrieves all possible neighboring cells (north, south, east, west) for a given cell.

    Args:
        cell (Tuple[int, int]): The current cell coordinates (row, col).

    Returns:
        List[Tuple[int, int]]: A list of neighboring cell coordinates.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E
    neighbors = []
    for dr, dc in directions:
        nr, nc = cell[0] + dr, cell[1] + dc
        if 0 <= nr < MAZE_SIZE and 0 <= nc < MAZE_SIZE:
            neighbors.append((nr, nc))
    return neighbors

def carve_passages_from(cell: Tuple[int, int], maze: List[List[str]], visited: List[List[bool]]):
    """
    Recursively carves passages in the maze starting from the given cell using the Recursive Backtracker algorithm.

    Args:
        cell (Tuple[int, int]): The current cell coordinates (row, col) in maze terms.
        maze (List[List[str]]): The 2D grid representing the maze.
        visited (List[List[bool]]): A 2D grid tracking visited cells.
    """
    stack = [cell]
    visited[cell[0]][cell[1]] = True

    while stack:
        current = stack[-1]
        neighbors = [n for n in get_neighbors(current) if not visited[n[0]][n[1]]]

        if neighbors:
            next_cell = random.choice(neighbors)
            visited[next_cell[0]][next_cell[1]] = True
            stack.append(next_cell)

            # Remove wall between current and next_cell
            wall_row = current[0] + next_cell[0] + 1
            wall_col = current[1] + next_cell[1] + 1
            maze[wall_row][wall_col] = PATH

            # Set path for the next_cell
            maze[2 * next_cell[0] + 1][2 * next_cell[1] + 1] = PATH
        else:
            stack.pop()

def generate_maze() -> List[List[str]]:
    """
    Generates a random maze with a guaranteed solution.

    Returns:
        List[List[str]]: A 2D grid representing the generated maze.
    """
    maze = initialize_maze()

    # Initialize visited cells grid
    visited = [[False for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

    # Start carving from the entrance cell (0,0)
    carve_passages_from((0, 0), maze, visited)

    # Set start and exit points
    maze[1][1] = START  # Entrance
    maze[GRID_SIZE - 2][GRID_SIZE - 2] = EXIT  # Exit

    # Open entrance and exit
    maze[0][1] = PATH  # Entrance opening
    maze[GRID_SIZE - 1][GRID_SIZE - 2] = PATH  # Exit opening

    return maze

def main():
    """
    Main function to generate and display the maze.
    """
    maze = generate_maze()
    print_maze(maze)

if __name__ == "__main__":
    main()
