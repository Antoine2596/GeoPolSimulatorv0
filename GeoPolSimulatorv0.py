import random
import pygame

# ----- CONFIG -----
MAP_WIDTH = 10
MAP_HEIGHT = 10
PIXEL_SIZE = 50
INITIAL_POP_PER_PIXEL = 1000
FPS = 1  # 1 frame = 1 year

COLORS = {
    'Alpha': (255, 0, 0),
    'Beta': (0, 0, 255),
    'Empty': (200, 200, 200)
}

# ----- CLASSES -----
class Country:
    def __init__(self, name, growth_rate, militarization, territory):
        self.name = name
        self.growth_rate = growth_rate
        self.militarization = militarization
        self.territory = set(territory)
        self.population = len(territory) * INITIAL_POP_PER_PIXEL
        self.army = int(self.population * self.militarization)

    def update_population(self):
        self.population = int(self.population * (1 + self.growth_rate))

    def update_army(self):
        self.army = int(self.population * self.militarization)

    def lose_territory(self, pixels):
        lost = set(random.sample(self.territory, min(len(self.territory), pixels)))
        self.territory -= lost
        self.population = len(self.territory) * INITIAL_POP_PER_PIXEL
        self.update_army()
        return lost

    def gain_territory(self, pixels):
        self.territory |= pixels
        self.population = len(self.territory) * INITIAL_POP_PER_PIXEL
        self.update_army()


# ----- FUNCTIONS -----
def simulate_war(attacker, defender):
    print(f"\nWAR: {attacker.name} attacks {defender.name}")
    if attacker.army > defender.army:
        loss_ratio = defender.army / attacker.army
        pixels_taken = int(len(defender.territory) * loss_ratio * 0.5)
        taken = defender.lose_territory(pixels_taken)
        attacker.gain_territory(taken)
        print(f"{attacker.name} wins and takes {len(taken)} pixels!")
    else:
        print(f"{defender.name} defends successfully.")


def draw_map(screen, countries):
    grid = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    for country in countries:
        for (x, y) in country.territory:
            grid[y][x] = country.name

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            owner = grid[y][x] or 'Empty'
            pygame.draw.rect(screen, COLORS[owner], (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((MAP_WIDTH * PIXEL_SIZE, MAP_HEIGHT * PIXEL_SIZE))
    pygame.display.set_caption("Territorial Simulator")
    clock = pygame.time.Clock()

    country_a = Country("Alpha", growth_rate=0.02, militarization=0.05,
                        territory={(x, y) for x in range(3) for y in range(3)})
    country_b = Country("Beta", growth_rate=0.015, militarization=0.07,
                        territory={(x, y) for x in range(7, 10) for y in range(7, 10)})

    countries = [country_a, country_b]

    running = True
    year = 0

    while running and year < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        year += 1
        print(f"\n--- Year {year} ---")
        for c in countries:
            c.update_population()
            c.update_army()
            print(f"{c.name}: pop={c.population}, army={c.army}, pixels={len(c.territory)}")

        if year % 3 == 0:
            simulate_war(country_a, country_b)

        screen.fill((255, 255, 255))
        draw_map(screen, countries)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()