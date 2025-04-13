from simulation import simulate_war

class WarManager:
    def __init__(self):
        self.active_wars = []  # list of tuples: (attacker, defender)
        self.conquered_pixels = {}  # map of (attacker, defender) → set of pixels
        self.defender_initial_territory = {}  # (attacker, defender) → nombre de pixels initiaux


    def declare_war(self, attacker, defender):
        key = (attacker, defender)
        if key not in self.active_wars:
            self.active_wars.append(key)
            self.conquered_pixels[key] = set()
            self.defender_initial_territory[key] = len(defender.territory)
            return f"{attacker.name} déclare la guerre à {defender.name}"
        return f"{attacker.name} est déjà en guerre avec {defender.name}"


    def update_wars(self):
        reports = []
        finished = []
        for attacker, defender in self.active_wars:
            initial_defender_pixels = self.defender_initial_territory.get(
                (attacker, defender), len(defender.territory)
            )

            conquered, result = simulate_war(
                attacker, defender,
                initial_defender_pixels=initial_defender_pixels
            )

            self.conquered_pixels[(attacker, defender)].update(conquered)
            reports.append(result)

            if result == "CAPITULATE" or len(defender.territory) == 0:
                finished.append((attacker, defender))

        for key in finished:
            attacker, defender = key
            gained = self.conquered_pixels[key]
            total_before = len(gained)
            final_gain = int(total_before * simulate_war.last_ratio / 10)
            kept = set(list(gained)[:final_gain])
            returned = gained - kept
            attacker.gain_territory(kept)
            defender.gain_territory(returned)
            self.active_wars.remove(key)
            del self.conquered_pixels[key]
            del self.defender_initial_territory[key]
            reports.append(f"{attacker.name} conserve {len(kept)} pixels, {defender.name} récupère {len(returned)}.")

        return reports


    def get_temp_conquests(self):
        # fusionne tous les pixels temporairement conquis
        temp_map = set()
        for conquered in self.conquered_pixels.values():
            temp_map.update(conquered)
        return temp_map