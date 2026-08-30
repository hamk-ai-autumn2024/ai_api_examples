import random

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

def create_maze(width, height):
    maze = [[Cell(x, y) for y in range(height)] for x in range(width)]
    stack = []
    current = maze[0][0]
    current.visited = True

    while True:
        unvisited = get_unvisited_neighbors(current, maze, width, height)
        if unvisited:
            next_cell = random.choice(unvisited)
            remove_wall(current, next_cell)
            stack.append(current)
            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break

    return maze

def get_unvisited_neighbors(cell, maze, width, height):
    neighbors = []
    directions = [('N', 0, -1), ('S', 0, 1), ('E', 1, 0), ('W', -1, 0)]

    for direction, dx, dy in directions:
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < width and 0 <= ny < height and not maze[nx][ny].visited:
            neighbors.append(maze[nx][ny])

    return neighbors

def remove_wall(cell1, cell2):
    dx = cell2.x - cell1.x
    dy = cell2.y - cell1.y

    if dx == 1:
        cell1.walls['E'] = False
        cell2.walls['W'] = False
    elif dx == -1:
        cell1.walls['W'] = False
        cell2.walls['E'] = False
    elif dy == 1:
        cell1.walls['S'] = False
        cell2.walls['N'] = False
    elif dy == -1:
        cell1.walls['N'] = False
        cell2.walls['S'] = False

def print_maze(maze, width, height):
    for y in range(height):
        # Print top walls
        for x in range(width):
            print('+', end='')
            print('-' if maze[x][y].walls['N'] else ' ', end='')
        print('+')

        # Print side walls
        for x in range(width):
            print('|' if maze[x][y].walls['W'] else ' ', end='')
            print(' ', end='')
        print('|')

    # Print bottom row
    for x in range(width):
        print('+', end='')
        print('-', end='')
    print('+')

# Create and print the maze
width, height = 20, 10
maze = create_maze(width, height)
print_maze(maze, width, height)
