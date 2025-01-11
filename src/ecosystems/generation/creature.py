from typing import List


class Creature:
    def __init__(self, affinities: List[str], family: str,
                 progression_path: str, creature_name="",
                 predators=[], prey=[],
                 speed=1, health=100, energy=100, energy_recovery=1) -> None:
        self.affinities = affinities
        self.family = family
        self.progression_path = progression_path
        self.name = creature_name

        self.predators = predators
        self.prey = prey

        # Needs, all go from [0, 100]
        self.hunger = 100
        self.thirst = 100
        self.sleep = 100

        # Traits
        self.speed = speed
        self.health = health
        self.energy = energy
        self.energy_recovery = energy_recovery

    def __str__(self) -> str:
        # Formatted for CSV output with columns:
        # 'CreatureName','Family','affinity1','affinity2','ProgressionPath','ProgressesFrom'
        # The 'ProgFrom' is not included in this string; see CreatureChain's __str__ method
        return f"{self.name},{self.family},{self.affinities[0]},{self.affinities[1]},{self.progression_path},"


class CreatureChain:
    def __init__(self, creatures: List[Creature]) -> None:
        self.creatures = creatures  # currently, always 3-stage

    def __str__(self) -> str:
        # Formatted for CSV output with columns:
        # 'CreatureName','Family1','Family2','affinity1','affinity2','ProgressionPath','EvolvesFrom'
        # Creates 3 rows separated by \n chars
        base_creature_str = str(self.creatures[0]) + ","  # no 'EvolvesFrom'
        middle_creature_str = str(self.creatures[1]) +\
            f",{self.creatures[0].name}"
        final_creature_str = str(self.creatures[2]) +\
            f",{self.creatures[1].name}"

        return f"{base_creature_str}\n{middle_creature_str}\n{final_creature_str}\n"
