import pygame as game
import random

window = 1000                                           # Set pop up window size
screen = game.display.set_mode([window] * 2)            # Sets screen dimensions
time, snake_can_move = 0, 75                            # Time will measure time elapsed since last snake movement
                                                        # snake_can_move checks if enough time has elapsed to move again
tile_size = 50                                          # Deciding 1 unit of movement and how large the snake/food is

# Creating snake, giving it a random starting position, and keeping it stationary
snake = game.rect.Rect([0, 0, tile_size, tile_size])
snake_pos_x = random.randrange(1, (window // tile_size)) * tile_size
snake_pos_y = random.randrange(1, (window // tile_size)) * tile_size
snake.center = (snake_pos_x, snake_pos_y)
snake_direction = (0, 0)

# Creating food and giving it a random starting position
food = game.rect.Rect([0, 0, tile_size, tile_size])
food_pos_x = random.randrange(1, (window // tile_size)) * tile_size
food_pos_y = random.randrange(1, (window // tile_size)) * tile_size
food.center = (food_pos_x, food_pos_y)


length = 1                                              # Determines how many segments of the snake there are
segments = [snake.copy()]                               # Holds each segment of the snake
clock = game.time.Clock()                               # Will be used to set fps

# Main event loop
while True:
    for event in game.event.get():
        # Decision tree for what program behavior based on user input
        if event.type == game.QUIT:                     # If user wants to quit
            exit()
        if event.type == game.KEYDOWN:                  # If user presses another key
            if event.key == game.K_UP and snake_direction != (0, tile_size):
                snake_direction = (0, -tile_size)       # If user goes up and snake is not moving down
            if event.key == game.K_DOWN and snake_direction != (0, -tile_size):
                snake_direction = (0, tile_size)        # If user goes down and snake is not moving up
            if event.key == game.K_LEFT and snake_direction != (tile_size, 0):
                snake_direction = (-tile_size, 0)       # If user goes left and snake is not moving right
            if event.key == game.K_RIGHT and snake_direction != (-tile_size, 0):
                snake_direction = (tile_size, 0)        # If user goes right and snake is not moving left

    screen.fill('black')                                # Setting black background for screen

    # If there is a collision between snake head and rest of it, self_colliding = False
    self_colliding = game.Rect.collidelist(snake, segments[:-1]) != -1

    # Bounds checking and checking if snake collides with itself
    if self_colliding or snake.top < 0 or snake.left < 0 or snake.right > window or snake.bottom > window:
        food_pos_x = random.randrange(1, (window // tile_size)) * tile_size
        food_pos_y = random.randrange(1, (window // tile_size)) * tile_size
        food.center = (food_pos_x, food_pos_y)          # Reset food
        snake_pos_x = random.randrange(1, (window // tile_size)) * tile_size
        snake_pos_y = random.randrange(1, (window // tile_size)) * tile_size
        snake.center = (snake_pos_x, snake_pos_y)       # Reset snake
        snake_direction = (0, 0)                        # Reset direction to none
        length, segments = 1, [snake.copy()]            # Reset length of snake

    # Handling snake eating food
    if snake.center == food.center:
        length += 1                                     # Increment length
        food_pos_x = random.randrange(1, (window // tile_size)) * tile_size
        food_pos_y = random.randrange(1, (window // tile_size)) * tile_size
        food.center = (food_pos_x, food_pos_y)          # Reset food

    # Draw snake
    [game.draw.rect(screen, 'green', segment) for segment in segments]

    # Draw food
    game.draw.rect(screen, 'red', food)

    # Move snake
    curr_time = game.time.get_ticks()
    if curr_time - time > snake_can_move:
        time = curr_time
        snake.move_ip(snake_direction)                  # move_ip() instead of move() to not compute new copy every time
        segments.append(snake.copy())
        segments = segments[-length:]                   # Draw segments based on length
    game.display.flip()                                 # Update screen
    clock.tick(120)                                     # Limit max FPS to 120
