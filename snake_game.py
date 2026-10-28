import random

import pygame

WINDOW_SIZE = 1000
TILE_SIZE = 50
MOVE_INTERVAL_MS = 75
MAX_FPS = 120

type Direction = tuple[int, int]

STOPPED: Direction = (0, 0)
KEY_DIRECTIONS: dict[int, Direction] = {
    pygame.K_UP: (0, -TILE_SIZE),
    pygame.K_DOWN: (0, TILE_SIZE),
    pygame.K_LEFT: (-TILE_SIZE, 0),
    pygame.K_RIGHT: (TILE_SIZE, 0),
}


def random_tile() -> pygame.Rect:
    """Return a tile-sized Rect centered on a random grid point inside the window."""
    tile = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    tile.center = (
        random.randrange(1, WINDOW_SIZE // TILE_SIZE) * TILE_SIZE,
        random.randrange(1, WINDOW_SIZE // TILE_SIZE) * TILE_SIZE,
    )
    return tile


def next_direction(current: Direction, key: int) -> Direction:
    """Return the direction for an arrow key, or `current` for any other key or a reversal."""
    requested = KEY_DIRECTIONS.get(key)
    if requested is None or requested == (-current[0], -current[1]):
        return current
    return requested


def play_round(screen: pygame.Surface, clock: pygame.time.Clock) -> bool:
    """Play until the snake hits a wall or itself; return False if the window was closed instead."""
    snake = random_tile()
    food = random_tile()
    direction = STOPPED
    length = 1
    segments = [snake.copy()]
    last_move_ms = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                direction = next_direction(direction, event.key)

        # The last segment is the head itself.
        hit_itself = snake.collidelist(segments[:-1]) != -1
        if hit_itself or not screen.get_rect().contains(snake):
            return True

        if snake.center == food.center:
            length += 1
            food = random_tile()

        screen.fill("black")
        for segment in segments:
            pygame.draw.rect(screen, "green", segment)
        pygame.draw.rect(screen, "red", food)
        pygame.display.flip()

        now_ms = pygame.time.get_ticks()
        if now_ms - last_move_ms > MOVE_INTERVAL_MS:
            last_move_ms = now_ms
            snake.move_ip(direction)  # in place, so a move doesn't make a new Rect
            segments.append(snake.copy())
            segments = segments[-length:]

        clock.tick(MAX_FPS)


def main() -> None:
    """Open the game window and start a new round after every crash, until the window is closed."""
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    while play_round(screen, clock):
        pass
    pygame.quit()


if __name__ == "__main__":
    main()
