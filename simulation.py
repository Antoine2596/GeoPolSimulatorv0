def simulate_war(attacker, defender):
    DEFENSE_BONUS = 1.0
    DAMAGE_RATIO = 0.2

    attacker_force = attacker.army
    defender_force = int(defender.army * DEFENSE_BONUS)
    
    if attacker_force < defender_force:
        # Inversion : le défenseur devient l'attaquant
        return simulate_war(defender, attacker)

    if defender_force == 0:
        simulate_war.last_ratio = 1  # valeur minimale
        simulate_war.total_pixels_before = len(defender.territory)
        return defender.territory.copy(), "CAPITULATE"


    attacker.population = max(0, attacker.population - int(DAMAGE_RATIO * defender_force))
    defender.population = max(0, defender.population - int(DAMAGE_RATIO * attacker_force))
    attacker.update_army()
    defender.update_army()

    ratio = attacker_force / defender_force
    percent_to_take = ratio / 100

    if initial_defender_pixels is None:
        initial_defender_pixels = len(defender.territory)

    pixels_to_take = max(1, int(initial_defender_pixels * percent_to_take))

    taken = defender.lose_territory(pixels_to_take)
    attacker.gain_territory(taken)

    simulate_war.last_ratio = ratio
    simulate_war.total_pixels_before = len(defender.territory) + len(taken)

    return taken, f"{attacker.name} prend {len(taken)} pixels à {defender.name} (ratio {ratio:.2f})"

simulate_war.last_ratio = 0
simulate_war.total_pixels_before = 0