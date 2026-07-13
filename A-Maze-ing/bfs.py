from print_maze import Cell
from collections import deque


def solve(maze: list[list[Cell]], entry: tuple[int, int],
          goal: tuple[int, int]) -> list[str]:
    """Find the shortest path from entry to goal using BFS.

    Args:
        maze: A list of lists of Cell objects representing the maze.
        entry: The (x, y) coordinates of the starting cell.
        goal: The (x, y) coordinates of the target cell.

    Returns:
        A list of directions (N, E, S, W) representing the shortest path.
    """
    cola: deque[tuple[int, int]] = deque()
    visitados = set()
    padres: dict[tuple[int, int], tuple[int, int]] = {}
    cola.append(entry)
    visitados.add(entry)
    while cola:
        x, y = cola.popleft()
        if (x, y) == goal:
            break
        cell = maze[y][x]
        if not cell.north and y - 1 >= 0 and (x, y - 1) not in visitados:
            visitados.add((x, y - 1))
            cola.append((x, y - 1))
            padres[(x, y - 1)] = (x, y)
        if not cell.east and (x + 1, y) not in visitados:
            visitados.add((x + 1, y))
            cola.append((x + 1, y))
            padres[(x + 1, y)] = (x, y)
        if not cell.south and (x, y + 1) not in visitados:
            visitados.add((x, y + 1))
            cola.append((x, y + 1))
            padres[(x, y + 1)] = (x, y)
        if not cell.west and x - 1 >= 0 and (x - 1, y) not in visitados:
            visitados.add((x - 1, y))
            cola.append((x - 1, y))
            padres[(x - 1, y)] = (x, y)
    path: list[str] = []
    current = goal
    while current != entry:
        parent = padres[current]
        dx = current[0] - parent[0]
        dy = current[1] - parent[1]
        if dx == 1:
            path.append("E")
        if dx == -1:
            path.append("W")
        if dy == 1:
            path.append("S")
        if dy == -1:
            path.append("N")
        current = parent
    path.reverse()
    return path


if __name__ == "__main__":
    maze = [[Cell() for _ in range(4)] for _ in range(4)]

# abrir camino hacia el este en la fila 0
maze[0][0].east = False
maze[0][1].west = False
maze[0][1].east = False
maze[0][2].west = False
maze[0][2].east = False
maze[0][3].west = False

# abrir camino hacia el sur en la columna 3
maze[0][3].south = False
maze[1][3].north = False
maze[1][3].south = False
maze[2][3].north = False
maze[2][3].south = False
maze[3][3].north = False
print(f"{solve(maze, (0,0), (3,3))}")