import pygame

from snake_game import (
    GRID_SIZE,
    KEY_DIRECTIONS,
    TILE_SIZE,
    next_direction,
    random_free_tile,
)


def test_food_never_spawns_under_the_snake() -> None:
    snake = [
        pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        for col in range(GRID_SIZE)
        for row in range(GRID_SIZE)
    ]
    only_free_tile = snake.pop(123)

    for _ in range(20):
        assert random_free_tile(snake) == only_free_tile


def test_two_turns_before_a_move_cannot_reverse_the_snake() -> None:
    right = KEY_DIRECTIONS[pygame.K_RIGHT]

    pending = next_direction(right, right, pygame.K_DOWN)
    pending = next_direction(pending, right, pygame.K_LEFT)

    assert pending == KEY_DIRECTIONS[pygame.K_DOWN]
