import pygame
import sys
from collections import deque
import math

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (255, 0, 0)

    def is_open(self):
        return self.color == (0, 255, 0)

    def is_barrier(self):
        return self.color == (0, 0, 0)

    def is_start(self):
        return self.color == (255, 165, 0)

    def is_end(self):
        return self.color == (255, 255, 0)

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = (255, 0, 0)

    def make_open(self):
        self.color = (0, 255, 0)

    def make_barrier(self):
        self.color = (0, 0, 0)

    def make_start(self):
        self.color = (255, 165, 0)

    def make_end(self):
        self.color = (255, 255, 0)

    def make_path(self):
        self.color = (0, 255, 255)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def bfs(draw, grid, start, end):
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        if current == end:
            for node in path:
                node.make_path()
            print("Path Found!")
            return True
        for neighbor in current.neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [current]))
                visited.add(neighbor)
                neighbor.make_open()
        draw()

    print("No path found.")
    return False

def dfs(draw, grid, start, end):
    visited = {start}
    stack = [(start, [])]

    while stack:
        current, path = stack.pop()
        if current == end:
            for node in path:
                node.make_path()
            print("Path Found!")
            return True
        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [current]))
                visited.add(neighbor)
                neighbor.make_open()
        draw()

    print("No path found.")
    return False



def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def astar(draw, grid, start, end):
    visited = {start}
    g_scores = {node: float("inf") for row in grid for node in row}
    g_scores[start] = 0
    f_scores = {node: float("inf") for row in grid for node in row}
    f_scores[start] = h(start.get_pos(), end.get_pos())
    queue = [(f_scores[start], start, [])]

    while queue:
        queue.sort(key=lambda x: x[0])
        f_score, current, path = queue.pop(0)
        if current == end:
            for node in path:
                node.make_path()
            print("Path Found!")
            return True
        for neighbor in current.neighbors:
            if neighbor not in visited:
                new_g_score = g_scores[current] + 1
                if new_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = new_g_score
                    f_scores[neighbor] = new_g_score + h(neighbor.get_pos(), end.get_pos())
                    queue.append((f_scores[neighbor], neighbor, path + [current]))
                    visited.add(neighbor)
                    neighbor.make_open()
        draw()

    print("No path found.")
    return False


def hill_climbing(draw, grid, start, end):
    current = start
    visited = {current}

    while current != end:
        next_node = None
        min_distance = float('inf')
        
        for neighbor in current.neighbors:
            if neighbor == end:
                neighbor.make_path()
                print("Path Found!")
                return True
            if neighbor.is_barrier() or neighbor in visited:
                continue
            neighbor_distance = h(neighbor.get_pos(), end.get_pos())
            if neighbor_distance < min_distance:
                min_distance = neighbor_distance
                next_node = neighbor
        
        if next_node is None:
            print("No path found.")
            return False
        
        next_node.make_open()
        current = next_node
        visited.add(current)
        draw()

    print("Path Found!")
    return True



def greedy_best_first(draw, grid, start, end):
    visited = {start}
    queue = [(h(start.get_pos(), end.get_pos()), start, [])]

    while queue:
        _, current, path = queue.pop(0)
        if current == end:
            for node in path:
                node.make_path()
            print("Path Found!")
            return True
        for neighbor in current.neighbors:
            if neighbor not in visited:
                queue.append((h(neighbor.get_pos(), end.get_pos()), neighbor, path + [current]))
                queue.sort(key=lambda x: x[0])
                visited.add(neighbor)
                neighbor.make_open()
        draw()

    print("No path found.")
    return False

def reset_grid(grid):
    for row in grid:
        for node in row:
            node.reset()

def draw_buttons():
    reset_button = pygame.Rect(20, HEIGHT - 50, 150, 30)
    pygame.draw.rect(window, GRAY, reset_button)
    font = pygame.font.Font(None, 24)
    text = font.render("Reset Grid", True, BLACK)
    window.blit(text, (30, HEIGHT - 45))

def main():
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    run_algorithm = False
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": astar,
        "Hill Climbing": hill_climbing,
        "Greedy Best First": greedy_best_first
    }
    selected_algorithm = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and selected_algorithm:
                    run_algorithm = True
                if event.key == pygame.K_r:
                    reset_grid(grid)
                    start = None
                    end = None
                    run_algorithm = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if 20 <= pos[0] <= 170 and HEIGHT - 50 <= pos[1] <= HEIGHT - 20:
                        reset_grid(grid)
                        start = None
                        end = None
                        run_algorithm = False
                    elif WIDTH - 160 <= pos[0] <= WIDTH and 20 <= pos[1] <= 20 + len(algorithms) * 30:
                        selected_algorithm = get_selected_algorithm(pos, algorithms)
                    else:
                        row, col = get_clicked_pos(pos, ROWS, WIDTH)
                        node = grid[row][col]
                        if not start and node != end:
                            start = node
                            start.make_start()
                        elif not end and node != start:
                            end = node
                            end.make_end()
                        elif node != end and node != start:
                            node.make_barrier()

        if pygame.mouse.get_pressed()[2]:  
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, WIDTH)
            node = grid[row][col]
            node.reset()
            if node == start:
                start = None
            elif node == end:
                end = None

        if run_algorithm and selected_algorithm:
            for row in grid:
                for node in row:
                    node.update_neighbors(grid)
            path_found = selected_algorithm(lambda: draw_grid(window, ROWS, WIDTH), grid, start, end)
            run_algorithm = False

        window.fill(WHITE)
        draw_grid(window, ROWS, WIDTH)
        for row in grid:
            for node in row:
                node.draw(window)
        draw_buttons()  # Draw buttons inside the main loop

        # Draw algorithm selection menu
        draw_menu(algorithms, selected_algorithm)

        pygame.display.update()

def get_selected_algorithm(pos, algorithms):
    menu_y = 20
    for algorithm_name, _ in algorithms.items():
        if WIDTH - 160 <= pos[0] <= WIDTH and menu_y <= pos[1] <= menu_y + 20:
            return algorithms[algorithm_name]
        menu_y += 30
    return None

def draw_menu(algorithms, selected_algorithm):
    font = pygame.font.Font(None, 24)
    menu_y = 20
    for algorithm_name, _ in algorithms.items():
        text = font.render(algorithm_name, True, BLACK if selected_algorithm == algorithms[algorithm_name] else GRAY)
        window.blit(text, (WIDTH - 160, menu_y))
        menu_y += 30

if __name__ == "__main__":
    main()

