import random

import pygame

WINDOW_SIZE = 1000
TILE_SIZE = 50
GRID_SIZE = WINDOW_SIZE // TILE_SIZE
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


def random_free_tile(occupied: list[pygame.Rect]) -> pygame.Rect:
    """Return a random grid tile that no Rect in `occupied` is on; at least one tile must be free."""
    taken = {rect.topleft for rect in occupied}
    every_tile = (
        (col * TILE_SIZE, row * TILE_SIZE)
        for col in range(GRID_SIZE)
        for row in range(GRID_SIZE)
    )
    free = [tile for tile in every_tile if tile not in taken]
    return pygame.Rect(random.choice(free), (TILE_SIZE, TILE_SIZE))


def next_direction(pending: Direction, moved: Direction, key: int) -> Direction:
    """Return the direction for an arrow key, or `pending` for any other key or a turn back along `moved`."""
    requested = KEY_DIRECTIONS.get(key)
    if requested is None or requested == (-moved[0], -moved[1]):
        return pending
    return requested


def show_score(score: int, best: int) -> None:
    """Show `score` and the best score so far in the title bar; `best` is the best of earlier rounds."""
    pygame.display.set_caption(f"Snake · Score {score} · Best {max(score, best)}")


def play_round(
    screen: pygame.Surface, clock: pygame.time.Clock, best: int
) -> int | None:
    """Play one round and return its score, or None if the window was closed."""
    show_score(0, best)
    snake = random_free_tile([])
    food = random_free_tile([snake])
    direction = STOPPED
    moved = STOPPED
    length = 1
    segments = [snake.copy()]
    last_move_ms = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                direction = next_direction(direction, moved, event.key)

        # The last segment is the head itself.
        hit_itself = snake.collidelist(segments[:-1]) != -1
        if hit_itself or not screen.get_rect().contains(snake):
            return length - 1

        if snake.center == food.center:
            length += 1
            show_score(length - 1, best)
            # The snake fills the board, so there's no tile left for food.
            if len(segments) == GRID_SIZE**2:
                return length - 1
            food = random_free_tile(segments)

        screen.fill("black")
        for segment in segments:
            pygame.draw.rect(screen, "green", segment)
        pygame.draw.rect(screen, "red", food)
        pygame.display.flip()

        now_ms = pygame.time.get_ticks()
        if now_ms - last_move_ms > MOVE_INTERVAL_MS:
            last_move_ms = now_ms
            snake.move_ip(direction)  # in place, so a move doesn't make a new Rect
            moved = direction
            segments.append(snake.copy())
            segments = segments[-length:]

        clock.tick(MAX_FPS)


def main() -> None:
    """Open the game window and play rounds, keeping the best score, until the window is closed."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    best = 0
    while (score := play_round(screen, clock, best)) is not None:
        best = max(best, score)
    pygame.quit()


if __name__ == "__main__":
    main()
