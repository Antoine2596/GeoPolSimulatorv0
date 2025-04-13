import pygame
from config import MAP_WIDTH, MAP_HEIGHT, PIXEL_SIZE, COLORS

def draw_map(screen, countries, temp_conquests):
    grid = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    for country in countries:
        for (x, y) in country.territory:
            grid[y][x] = country.name

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            pos = (x, y)
            if pos in temp_conquests:
                color = (255, 255, 0)  # Jaune = territoire temporairement occupé
            else:
                owner = grid[y][x] or 'Empty'
                color = COLORS[owner]
            pygame.draw.rect(screen, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 1)
