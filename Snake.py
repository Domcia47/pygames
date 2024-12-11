import sys
import pygame
import random
import queue

# COLORS
black = (0, 0, 0)
gray = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
bright_violet = (238, 130, 238)

# INITIALIZE THE GAME
pygame.init()
size = width, height = (300, 300)
dashboard_height = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')

# CLOCK
speed_increment = 0.5
FPS = 10
clock = pygame.time.Clock()

# VARIABLES
current_speed = [0, -10]
head = pygame.Rect(width / 2, (height + dashboard_height) / 2, 10, 10)  # Snake head
generate_new_food = True
good_food = None  #Rect for good food
bad_food = None  #Rect for bad food
gained_score = None
score = 0  #Initial score
time = 0
time_limit = 400
snake_body = queue.Queue()

# MAIN GAME LOOP
while True:
    # HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
            mouse_x, mouse_y = event.pos  # Get mouse click coordinates
            # Check which region the click is in relative to the snake's head
            if mouse_x < head.x and abs(mouse_x - head.x) > abs(mouse_y - head.y):  # Click to the left
                current_speed = [-10, 0]  # Move left
            elif mouse_x > head.x + head.width and abs(mouse_x - head.x) > abs(mouse_y - head.y):  # Click to the right
                current_speed = [10, 0]  # Move right
            elif mouse_y < head.y:  # Click above
                current_speed = [0, -10]  # Move up
            elif mouse_y > head.y + head.height:  # Click below
                current_speed = [0, 10]  # Move down

    # Check game over condition
    if score < 0:
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("GAME OVER", True, red)
        screen.fill(black)
        text_width = game_over_text.get_width()
        text_height = game_over_text.get_height()
        screen.blit(game_over_text, ((width - text_width) // 2, (height - text_height) // 2))
        pygame.display.flip()
        continue

    # Check win condition
    if score >= 150:
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("YOU WON", True, green)
        screen.fill(black)

        text_width = win_text.get_width()
        text_height = win_text.get_height()
        screen.blit(win_text, ((width - text_width) // 2, (height - text_height) // 2))
        pygame.display.flip()
        continue

    # Generate food if needed
    if generate_new_food:
        food_size = 10
        random_x_good = random.randint(0, width - food_size)
        random_y_good = random.randint(dashboard_height, height - food_size)
        good_food = pygame.Rect(random_x_good, random_y_good, food_size, food_size)

        random_x_bad = random.randint(0, width - food_size)
        random_y_bad = random.randint(dashboard_height, height - food_size)
        bad_food = pygame.Rect(random_x_bad, random_y_bad, food_size, food_size)

        time = 0
        generate_new_food = False
        if gained_score and score % 10 == 0:
            FPS = min(25,FPS+speed_increment)
            time_limit = max(200, time_limit - 2) 

    # Move the snake's head
    head = head.move(current_speed)

    if head.left < 0:  # Move from left to right
        head.left = width
    elif head.right > width:  # Move from right to left
        head.right = 0
    if head.top < dashboard_height:  # Move from top to bottom
        head.top = height
    elif head.bottom > height:  # Move from bottom to top
        head.bottom = dashboard_height
    
    # Check collision with good food
    if head.colliderect(good_food):
        score += 5 
        generate_new_food = True 
        gained_score = True

    # Check collision with bad food
    if head.colliderect(bad_food):
        score -= 15 
        generate_new_food = True

    # DRAWING
    screen.fill(black)
    pygame.draw.line(screen, white, (0, dashboard_height), (width, dashboard_height))
    pygame.draw.rect(screen, blue, head)  #Snake head
    if good_food:
        pygame.draw.rect(screen, bright_violet, good_food)  #Draw good food
    if bad_food:
        pygame.draw.rect(screen, green, bad_food)  #Draw bad food

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Life points: {score}", True, white)
    screen.blit(score_text, (10, 10))
    time += 10  # Increment the timer

    # Regenerate food after a certain time
    if time >= time_limit:
        generate_new_food = True

    pygame.display.flip()
    clock.tick(FPS)
