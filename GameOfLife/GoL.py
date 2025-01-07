import sys
import pygame
import random
from collections import deque
# COLORS
black = (0, 0, 0)
white = (255, 255, 255)

# INITIALIZE THE GAME
pygame.init()
size = width, height = (1100,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game of Life')

# CLOCK
FPS = 1
clock = pygame.time.Clock()

# VARIABLES
cell_size = 10

# CELLS MATRIX 
matrix_size = matrix_width, matrix_height = (width//cell_size,height//cell_size)
cells= [[random.randint(0, 1) for _ in range(matrix_width)] for _ in range(matrix_height)]

last_col_idx = matrix_width - 1
last_row_idx = matrix_height - 1

def draw_cells():
    for row in range(matrix_height):
        for col in range(matrix_width):
            color = white if cells[row][col] == 1 else black
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

def check_neighbors(cell_row, cell_col):
    living_neighbors = 0
    if cell_row - 1 >= 0:
        if cells[cell_row - 1][cell_col] == 1:
            living_neighbors += 1
    if cell_col - 1 >= 0:
        if cells[cell_row][cell_col - 1] == 1:
            living_neighbors += 1
    if cell_row + 1 <= last_row_idx:
        if cells[cell_row + 1][cell_col] == 1:
            living_neighbors += 1
    if cell_col + 1 <= last_col_idx:
        if cells[cell_row][cell_col + 1] == 1:
            living_neighbors += 1
        # Sprawdzenie sąsiadów po przekątnych
    if cell_row - 1 >= 0 and cell_col - 1 >= 0:
        if cells[cell_row - 1][cell_col - 1] == 1:  # Górny lewy
            living_neighbors += 1
    if cell_row - 1 >= 0 and cell_col + 1 <= last_col_idx:
        if cells[cell_row - 1][cell_col + 1] == 1:  # Górny prawy
            living_neighbors += 1
    if cell_row + 1 <= last_row_idx and cell_col - 1 >= 0:
        if cells[cell_row + 1][cell_col - 1] == 1:  # Dolny lewy
            living_neighbors += 1
    if cell_row + 1 <= last_row_idx and cell_col + 1 <= last_col_idx:
        if cells[cell_row + 1][cell_col + 1] == 1:  # Dolny prawy
            living_neighbors += 1
    return living_neighbors

def calulate_next_state():
    new_cells = [[cells[row][col] for col in range(matrix_width)] for row in range(matrix_height)]
    
    for row in range(matrix_height):
        for col in range(matrix_width):
            living_neighbors = check_neighbors(row, col)
            if cells[row][col] == 0 and living_neighbors == 3:
                new_cells[row][col] = 1  # Martwa komórka staje się żywa
            elif cells[row][col] == 1 and not (living_neighbors == 3 or living_neighbors == 2):
                new_cells[row][col] = 0  # Żywa komórka staje się martwa
    
    # Zaktualizuj oryginalną macierz komórek
    for row in range(matrix_height):
        for col in range(matrix_width):
            cells[row][col] = new_cells[row][col]
    
# MAIN GAME LOOP
while True:
    # HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
         
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Pobierz pozycję myszy
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Przelicz współrzędne myszy na współrzędne w macierzy
            col = mouse_x // cell_size
            row = mouse_y // cell_size
            
            # Zmień stan klikniętej komórki
            if cells[row][col] == 0:
                cells[row][col] = 1  # Martwa komórka staje się żywa
            else:
                cells[row][col] = 0  # Żywa komórka staje się martwa
    
    screen.fill(black)
    draw_cells()
    calulate_next_state()
    pygame.display.flip()
    clock.tick(FPS)
