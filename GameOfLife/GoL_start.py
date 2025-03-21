import sys
import pygame
from GoL import PlayRandomBoard,PlayCustomBoard
# COLORS
black = (0, 0, 0)
white = (255, 255, 255)

# INITIALIZE THE GAME
pygame.init()
size = width, height = (1100, 700)
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption('Game of Life')

def get_font(size):  # Returns font in the desired size
    return pygame.font.Font("font.ttf", size)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    SCREEN.blit(text_surface, text_rect)

def main_menu():
    MENU_MOUSE_POS = (0,0)
    
    while True:
        SCREEN.fill(black)

        # "MAIN MENU" text
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b6ed48")
        MENU_RECT = MENU_TEXT.get_rect(center=(width // 2 + 10, 110))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Buttons' texts and their positions
        draw_board_text = get_font(50).render("DRAW BOARD", True, "#d7fcd4")
        draw_board_rect = draw_board_text.get_rect(center=(width // 2, 260))

        random_board_text = get_font(50).render("RANDOM BOARD", True, "#d7fcd4")
        random_board_rect = random_board_text.get_rect(center=(width // 2, 410))

        quit_text = get_font(50).render("QUIT", True, "#d7fcd4")
        quit_rect = quit_text.get_rect(center=(width // 2, 560))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                MENU_MOUSE_POS = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_board_rect.collidepoint(MENU_MOUSE_POS):
                    draw_board()
                if random_board_rect.collidepoint(MENU_MOUSE_POS):
                    random_board()
                if quit_rect.collidepoint(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Hover effect: change color when mouse is over the button
        if draw_board_rect.collidepoint(MENU_MOUSE_POS):
            draw_board_text = get_font(50).render("DRAW BOARD", True, "White")
        if random_board_rect.collidepoint(MENU_MOUSE_POS):
            random_board_text = get_font(50).render("RANDOM BOARD", True, "White")
        if quit_rect.collidepoint(MENU_MOUSE_POS):
            quit_text = get_font(50).render("QUIT", True, "White")

        # Draw the buttons
        SCREEN.blit(draw_board_text, draw_board_rect)
        SCREEN.blit(random_board_text, random_board_rect)
        SCREEN.blit(quit_text, quit_rect)


        pygame.display.update()

def random_board():
    game = PlayRandomBoard()
    game.run()

def draw_board():
    game = PlayCustomBoard() 
    game.run()

if __name__ == "__main__":
    if len(sys.argv)>1:
        filename = sys.argv[1]
        game = PlayCustomBoard(filename) 
        game.run()
    else:    
        main_menu()
