from config import INITIAL_POP_PER_PIXEL
import random

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
        lost = set(random.sample(sorted(self.territory), min(len(self.territory), pixels)))
        self.territory -= lost
        # Supprime juste les pixels, sans modifier la population
        return lost

    def gain_territory(self, pixels):
        self.territory |= pixels
