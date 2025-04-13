import pygame
from config import *
from country import Country
from map import draw_map
from war_manager import WarManager

pygame.init()
screen = pygame.display.set_mode((MAP_WIDTH * PIXEL_SIZE, MAP_HEIGHT * PIXEL_SIZE + 100))
pygame.display.set_caption("Territorial Simulator")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

half = MAP_WIDTH // 2
territory_a = {(x, y) for x in range(half) for y in range(MAP_HEIGHT)}
territory_b = {(x, y) for x in range(half, MAP_WIDTH) for y in range(MAP_HEIGHT)}

country_a = Country("Alpha", 0.0, 0.01, territory_a)
country_b = Country("Beta", 0.0, 0.02, territory_b)
countries = [country_a, country_b]

war_manager = WarManager()
running = True
year = 0
message = ""

while running and year < 1000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                message = war_manager.declare_war(country_a, country_b)

    year += 1
    for c in countries:
        c.update_population()
        c.update_army()



    war_reports = war_manager.update_wars()
    if war_reports:
        message = war_reports[-1]

    screen.fill((255, 255, 255))
    temp = war_manager.get_temp_conquests()
    draw_map(screen, countries, temp)

    pygame.draw.rect(screen, (220, 220, 220), (0, MAP_HEIGHT * PIXEL_SIZE, MAP_WIDTH * PIXEL_SIZE, 100))
    text_lines = [
        f"Year: {year}",
        f"Alpha - Pop: {country_a.population}, Army: {country_a.army}, Pixels: {len(country_a.territory)}",
        f"Beta - Pop: {country_b.population}, Army: {country_b.army}, Pixels: {len(country_b.territory)}",
        f"Press SPACE to declare war",
        message
    ]
    for i, line in enumerate(text_lines):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (10, MAP_HEIGHT * PIXEL_SIZE + 5 + i * 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()