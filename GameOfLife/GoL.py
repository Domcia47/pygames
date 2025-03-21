import sys
import pygame
import random

# COLORS
black = (0, 0, 0)
white = (255, 255, 255)
class PlayBoard:
    def __init__(self, is_random=True, filename = ""):
        # INITIALIZE THE GAME
        self.size = self.width, self.height = (1100, 700)
        self.screen = pygame.display.set_mode(self.size)
        
        # CLOCK
        self.FPS = 5
        self.clock = pygame.time.Clock()

        # VARIABLES
        self.cell_size = 10

        # CELLS MATRIX 
        self.matrix_width, self.matrix_height = (self.width // self.cell_size, self.height // self.cell_size)
        
        # matrix inicialization - random or drawing
        self.cells = self.initialize_cells(is_random,filename)

        self.last_col_idx = self.matrix_width - 1
        self.last_row_idx = self.matrix_height - 1

    def initialize_cells(self, is_random, filename):
        if filename!="":
            cells = []
            try:
                with open(filename, 'r') as file:
                    for line in file:
                        row = list(map(int,line.split()))
                        cells.append(row)
            except FileNotFoundError:
                ("File not found")
                sys.exit(1)
            return cells
        if is_random:
            return [[random.randint(0, 1) for _ in range(self.matrix_width)] for _ in range(self.matrix_height)]
        else:
            return [[0 for _ in range(self.matrix_width)] for _ in range(self.matrix_height)]  # Start with all cells dead
            

    def draw_cells(self):
        for row in range(self.matrix_height):
            for col in range(self.matrix_width):
                color = white if self.cells[row][col] == 1 else black
                pygame.draw.rect(self.screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

    def check_neighbors(self, cell_row, cell_col):
        living_neighbors = 0
        if cell_row - 1 >= 0 and self.cells[cell_row - 1][cell_col] == 1:
            living_neighbors += 1
        if cell_col - 1 >= 0 and self.cells[cell_row][cell_col - 1] == 1:
            living_neighbors += 1
        if cell_row + 1 <= self.last_row_idx and self.cells[cell_row + 1][cell_col] == 1:
            living_neighbors += 1
        if cell_col + 1 <= self.last_col_idx and self.cells[cell_row][cell_col + 1] == 1:
            living_neighbors += 1
        # Check diagonal neighbors
        if cell_row - 1 >= 0 and cell_col - 1 >= 0 and self.cells[cell_row - 1][cell_col - 1] == 1:
            living_neighbors += 1
        if cell_row - 1 >= 0 and cell_col + 1 <= self.last_col_idx and self.cells[cell_row - 1][cell_col + 1] == 1:
            living_neighbors += 1
        if cell_row + 1 <= self.last_row_idx and cell_col - 1 >= 0 and self.cells[cell_row + 1][cell_col - 1] == 1:
            living_neighbors += 1
        if cell_row + 1 <= self.last_row_idx and cell_col + 1 <= self.last_col_idx and self.cells[cell_row + 1][cell_col + 1] == 1:
            living_neighbors += 1
        return living_neighbors

    def calculate_next_state(self):
        new_cells = [[self.cells[row][col] for col in range(self.matrix_width)] for row in range(self.matrix_height)]
        
        for row in range(self.matrix_height):
            for col in range(self.matrix_width):
                living_neighbors = self.check_neighbors(row, col)
                if self.cells[row][col] == 0 and living_neighbors == 3:
                    new_cells[row][col] = 1  # Dead cell becomes alive
                elif self.cells[row][col] == 1 and not (living_neighbors == 3 or living_neighbors == 2):
                    new_cells[row][col] = 0  # Alive cell becomes dead
        
        # Update the original cell matrix
        for row in range(self.matrix_height):
            for col in range(self.matrix_width):
                self.cells[row][col] = new_cells[row][col]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_x, mouse_y = event.pos

                # Convert mouse position to matrix coordinates
                col = mouse_x // self.cell_size
                row = mouse_y // self.cell_size

                # Toggle the state of the clicked cell
                self.cells[row][col] = 0 if self.cells[row][col] == 1 else 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start the game
                    self.run()

    def run(self):
        while True:
            self.screen.fill(black)
            self.handle_events()
            self.draw_cells()
            self.calculate_next_state()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def matrix_to_file(self):
        with open("cells.txt", 'w') as file:
            for row in self.cells:
                file.write(' '.join(map(str,row))+'\n')

class PlayRandomBoard(PlayBoard):
    def __init__(self):
        super().__init__(is_random=True)


class PlayCustomBoard(PlayBoard):
    def __init__(self,filename=""):
        super().__init__(is_random=False, filename=filename)
        self.accepted_board = False
    
    def run(self):
        while True:
            self.screen.fill(black)
            self.draw_cells()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(self.FPS)
                
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_x, mouse_y = event.pos

                col = mouse_x // self.cell_size
                row = mouse_y // self.cell_size

                # Change the state of the clicked cell
                if self.cells[row][col] == 1:
                    self.cells[row][col] = 0 
                else:
                    self.cells[row][col] = 1

            if event.type == pygame.KEYDOWN and not self.accepted_board:
                if event.key == pygame.K_RETURN:  # Press Enter to start the game
                    self.accepted_board = True
                    self.matrix_to_file()
                    super().run()

