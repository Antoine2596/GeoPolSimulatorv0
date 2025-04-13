from simulation import simulate_war

class WarManager:
    def __init__(self):
        self.active_wars = []
        self.conquered_pixels = {}
        self.defender_initial_territory = {}

    def declare_war(self, attacker, defender):
        key = (attacker, defender)

        if len(attacker.territory) == 0:
            return f"{attacker.name} ne peut pas déclarer de guerre sans territoire."
        if len(defender.territory) == 0:
            return f"{defender.name} n'a plus de territoire. Guerre impossible."

        if key not in self.active_wars:
            self.active_wars.append(key)
            self.conquered_pixels[key] = set()
            self.defender_initial_territory[key] = len(defender.territory)
            return f"{attacker.name} déclare la guerre à {defender.name}"

        return f"{attacker.name} est déjà en guerre avec {defender.name}"

    def update_wars(self):
        reports = []
        finished = []
        war_ratios = {}

        for attacker, defender in self.active_wars:
            key = (attacker, defender)

            if len(defender.territory) == 0:
                reports.append(f"{defender.name} n'a plus de territoire. Capitulation.")
                finished.append((attacker, defender))
                war_ratios[key] = 1.0
                continue

            initial_defender_pixels = self.defender_initial_territory.get(key, len(defender.territory))
            conquered, result, ratio = simulate_war(attacker, defender, initial_defender_pixels)
            self.conquered_pixels[key].update(conquered)
            war_ratios[key] = ratio
            reports.append(result)

            if result == "CAPITULATE":
                finished.append((attacker, defender))

        for key in finished:
            attacker, defender = key
            gained = self.conquered_pixels[key]
            total_before = len(gained)
            ratio = war_ratios.get(key, 1.0)
            final_gain = max(1, int(total_before * min(ratio, 1.0)))
            kept = set(list(gained)[:final_gain])
            returned = gained - kept

            attacker.gain_territory(kept)
            defender.gain_territory(returned)

            self.active_wars.remove(key)
            del self.conquered_pixels[key]
            if key in self.defender_initial_territory:
                del self.defender_initial_territory[key]

            reports.append(f"{attacker.name} conserve {len(kept)} pixels, {defender.name} récupère {len(returned)}.")

        return reports

    def get_temp_conquests(self):
        temp_map = set()
        for conquered in self.conquered_pixels.values():
            temp_map.update(conquered)
        return temp_map