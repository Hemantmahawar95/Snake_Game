import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Window size
display_width = 800
display_height = 600

# Create display window
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Create directory for assets if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def create_food():
    """Creates food at a random position"""
    food_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    return food_x, food_y


def our_snake(snake_block, snake_list):
    """Draw the snake"""
    for x in snake_list:
        pygame.draw.rect(game_display, green, [x[0], x[1], snake_block, snake_block])
        # Draw eyes
        eye_radius = snake_block // 5
        pygame.draw.circle(game_display, black, (int(x[0] + snake_block * 3/4), int(x[1] + snake_block/3)), eye_radius)
        pygame.draw.circle(game_display, black, (int(x[0] + snake_block * 3/4), int(x[1] + snake_block*2/3)), eye_radius)
        
        # If it's the head, draw a tongue
        if x == snake_list[-1]:
            pygame.draw.line(game_display, red, 
                            (x[0] + snake_block, x[1] + snake_block/2), 
                            (x[0] + snake_block*1.5, x[1] + snake_block/2), 2)
            pygame.draw.line(game_display, red, 
                            (x[0] + snake_block*1.5, x[1] + snake_block/2), 
                            (x[0] + snake_block*1.7, x[1] + snake_block/3), 2)
            pygame.draw.line(game_display, red, 
                            (x[0] + snake_block*1.5, x[1] + snake_block/2), 
                            (x[0] + snake_block*1.7, x[1] + snake_block*2/3), 2)


def draw_food(x, y):
    """Draw food with appealing design"""
    # Draw apple-like food
    pygame.draw.circle(game_display, red, (x + snake_block//2, y + snake_block//2), snake_block//2)
    # Draw stem
    pygame.draw.rect(game_display, (139, 69, 19), [x + snake_block//2 - 2, y, 4, 5])
    # Draw leaf
    pygame.draw.ellipse(game_display, green, [x + snake_block//2 + 2, y, 8, 6])


def show_score(score):
    """Display score value"""
    value = score_font.render("Score: " + str(score), True, black)
    game_display.blit(value, [10, 10])


def message(msg, color, y_displace=0):
    """Display a message on screen"""
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [display_width / 6, display_height / 3 + y_displace])


def draw_background():
    """Draw a nice background with grass pattern"""
    # Sky
    game_display.fill((135, 206, 235))  # Light blue
    
    # Ground
    pygame.draw.rect(game_display, (34, 139, 34), [0, display_height-100, display_width, 100])
    
    # Grass tufts
    for i in range(0, display_width, 50):
        pygame.draw.polygon(game_display, (0, 100, 0), 
                           [(i, display_height-100), (i+10, display_height-120), (i+20, display_height-100)])
    
    # Sun
    pygame.draw.circle(game_display, (255, 255, 0), (50, 50), 30)
    
    # Clouds
    for cloud_x in [200, 500]:
        pygame.draw.circle(game_display, white, (cloud_x, 80), 25)
        pygame.draw.circle(game_display, white, (cloud_x + 20, 70), 25)
        pygame.draw.circle(game_display, white, (cloud_x + 40, 80), 25)


def game_loop():
    """Main game loop"""
    game_over = False
    game_close = False

    # Starting position
    x1 = display_width / 2
    y1 = display_height / 2

    # Change of position
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Generate first food
    food_x, food_y = create_food()

    # Direction (initially not moving)
    direction = ''

    while not game_over:

        while game_close:
            game_display.fill(white)
            message("You Lost! Press C-Play Again or Q-Quit", red, -50)
            message("Your Score: " + str(length_of_snake - 1), black, 0)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'DOWN'

        # Check if snake hits boundary
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Draw background and game elements
        draw_background()
        draw_food(food_x, food_y)
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        # Remove the oldest segment if the snake hasn't grown
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake
        our_snake(snake_block, snake_list)
        
        # Show score
        show_score(length_of_snake - 1)

        pygame.display.update()

        # Check if snake eats food
        if x1 == food_x and y1 == food_y:
            food_x, food_y = create_food()
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Start the game
game_loop() 
