def simulate_war(attacker, defender, initial_defender_pixels=None):
    if len(defender.territory) == 0:
        ratio = attacker.army / max(defender.army, 1)
        return set(), "CAPITULATE", min(ratio, 1.0)

    DEFENSE_BONUS = 1.5
    DAMAGE_RATIO = 0.2

    attacker_force = attacker.army
    defender_force = int(defender.army * DEFENSE_BONUS)

    if attacker_force < defender_force:
        return simulate_war(defender, attacker, initial_defender_pixels)

    attacker.population = max(0, attacker.population - int(DAMAGE_RATIO * defender_force))
    defender.population = max(0, defender.population - int(DAMAGE_RATIO * attacker_force))
    attacker.update_army()
    defender.update_army()

    ratio = attacker_force / max(defender_force, 1)

    if initial_defender_pixels is None:
        initial_defender_pixels = len(defender.territory)

    percent_to_take = ratio / 100
    pixels_to_take = max(1, int(initial_defender_pixels * percent_to_take))
    pixels_to_take = min(pixels_to_take, len(defender.territory))

    taken = defender.lose_territory(pixels_to_take)
    attacker.gain_territory(taken)

    return taken, f"{attacker.name} prend {len(taken)} pixels à {defender.name} (ratio {ratio:.2f})", min(ratio, 1.0)