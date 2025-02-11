# Read the "creature_traits.json" and create new creatures based on
# combinations of animal families and affinities. Should create every
# possible combination as a 3-stage, then I can filter out the ones that
# don't make sense
from copy import deepcopy
import json
import networkx as nx
import numpy as np
import random
from typing import Dict, List

from ecosystems.generation.creature import Creature, CreatureChain
from ecosystems.generation.probability import generate_from_list, generate_potential_pair, weighted_randint
from ecosystems.viz.pgv_nx import visualize_taxonomy


SEED = 420
random.seed(SEED)
np.random.seed(SEED)


def read_traits_json(json_file: str) -> Dict:
    with open(json_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    return data


def generate_creature(animal_affinities: List[str],
                      animal_families: List[str],
                      progression_path="Random",
                      secondary_affinity_chance=0.25,
                      secondary_family_chance=0.5,
                      name_prefix="") -> Creature:
    # Generate a single creature
    # affinities are all the potential affinities to consider when creating
    # chains. The Base affinity will remain throughout, there is a
    # "secondary_affinity_chance"
    # chance that a secondary affinity is picked at each stage
    # animal_families: all possible animal families, will choose 1 or 2 to
    # base the creature
    # prog_path is either "natural", "robotic", "mixed", "random"; if
    # "random", pick one of the 3 with equal chance; this is fixed across
    # chain
    affinities = generate_potential_pair(animal_affinities,
                                         secondary_affinity_chance)
    families = random.choice(animal_families)

    if progression_path == "Random":
        progression_path = random.choice(["Natural", "Robotic", "Mixed"])

    creature = Creature(affinities, families,
                        progression_path, f"{name_prefix}")
    return creature


def create_evolution_chain(animal_affinities: List[str],
                           animal_families: List[str],
                           progression_path="Random",
                           secondary_affinity_chance=0.25,
                           secondary_family_chance=0.5,
                           name_prefix="") -> CreatureChain:
    # Generate a 3-stage evolution chain'
    # affinities are all the potential affinities to consider when creating
    # chains. The Base affinity will remain throughout, there is a
    # "secondary_affinity_chance"
    # chance that a secondary affinity is picked at each stage
    # animal_families: all possible animal families, will choose 1 or 2 to
    # base the creature
    # prog_path is either "natural", "robotic", "mixed", "random"; if
    # "random", pick one of the 3 with equal chance; this is fixed across
    # chain
    affinities = deepcopy(animal_affinities)
    families = deepcopy(animal_families)
    # Base creature:
    base_creature = generate_creature(affinities, families,
                                      progression_path=progression_path,
                                      secondary_affinity_chance=secondary_affinity_chance,
                                      secondary_family_chance=secondary_family_chance,
                                      name_prefix=f"{name_prefix}1")
    # Middle creature:
    # primary affinity is fixed, secondary can still be set if it was
    # empty before
    affinities.remove(base_creature.affinities[0])
    families.remove(base_creature.family[0])
    creature_affinities = deepcopy(base_creature.affinities)
    creature_families = deepcopy(base_creature.family)
    if not creature_affinities[1]:
        creature_affinities[1] = generate_from_list(affinities,
                                                    secondary_affinity_chance)

    if not creature_families[1]:
        creature_families[1] = generate_from_list(families,
                                                  secondary_family_chance)

    # progression path is fixed
    middle_creature = Creature(deepcopy(creature_affinities),
                               deepcopy(creature_families),
                               base_creature.progression_path,
                               creature_name=f"{name_prefix}2")

    # Final form:
    # same rules as for middle
    creature_affinities = deepcopy(middle_creature.affinities)
    creature_families = deepcopy(middle_creature.family)
    if not creature_affinities[1]:
        creature_affinities[1] = generate_from_list(affinities,
                                                    secondary_affinity_chance)

    if not creature_families[1]:
        creature_families[1] = generate_from_list(families,
                                                  secondary_family_chance)

    # progression path is fixed
    final_creature = Creature(deepcopy(creature_affinities),
                              deepcopy(creature_families),
                              base_creature.progression_path,
                              creature_name=f"{name_prefix}2")

    return CreatureChain([base_creature, middle_creature, final_creature])


def write_random_creature_chains(traits: Dict, num_iter: int,
                                 output_file: str) -> List[CreatureChain]:
    creature_chains = []
    for i in range(num_iter):
        creature_chains.append(create_evolution_chain(traits["affinity"],
                                                      traits["family"],
                                                      secondary_affinity_chance=0.5,
                                                      secondary_family_chance=0.5,
                                                      name_prefix=f"{i}_"))

    # (Over)write to file
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Header
        outfile.write(
            "CreatureName,Family1,Family2,affinity1,affinity2,ProgressionPath,EvolvesFrom\n")
        # Creature chains
        for chain in creature_chains:
            outfile.write(str(chain))

    return creature_chains


def generate_taxonomy(traits: Dict, num_base: int, max_middle_branches: int,
                      max_final_branches: int) -> nx.MultiDiGraph:
    # Create a multidigraph of taxonomy by generating a base creature &
    # branching off based on affinity and family
    # 1 base creature per progression path, which is fixed throughout
    # Base creatures only have 1 affinity and 1 family
    # Generate 1 middle creature for each potential family
    all_affinities = traits["affinity"]
    all_families = traits["family"]
    taxonomy = nx.MultiDiGraph()
    progression_paths = ["Natural", "Mixed", "Robotic"]
    for i in range(num_base):
        # Generate base creature
        # Primary attributes for this chain
        primary_affinity = generate_from_list(all_affinities, 1.)
        family = generate_from_list(all_families, 1)
        # Create and add to taxonomy
        for j, progression in enumerate(progression_paths):
            base_creature = Creature([primary_affinity, ""],
                                     family, progression,
                                     creature_name=f"{SEED}_{i}")
            taxonomy.add_node(base_creature)
            base_name = base_creature.name
            # Generate middle creature choices for this chain
            num_middle = weighted_randint(1, max_middle_branches)
            # Randomly pick potential families for middle chains
            for k in range(num_middle):
                middle_creature = Creature([primary_affinity, ""],
                                           family,
                                           progression,
                                           creature_name=f"{base_name}_{k}")
                taxonomy.add_edge(base_creature, middle_creature)
                base_name = middle_creature.name
                # Generate final creature choices for this chain
                num_final = weighted_randint(1, max_final_branches)
                # Randomly pick potential affinities for final chains
                secondary_affinities = [""] +\
                    random.sample([a for a in all_affinities
                                   if not a in base_creature.affinities],
                                  num_final)
                for l, secondary_affinity in enumerate(secondary_affinities):
                    final_creature = Creature([primary_affinity, secondary_affinity],
                                              family,
                                              progression,
                                              creature_name=f"{base_name}_{l}")
                    taxonomy.add_edge(middle_creature, final_creature)

    return taxonomy


def main():
    traits_file = "../res/creature_traits.json"
    traits_data = read_traits_json(traits_file)

    # Write out random creatures in chains as potential inspiration
    # building blocks
    # creature_chains = write_random_creature_chains(traits_data, 100,
    #                                                "../out/random_creatures.csv")

    # Creature taxonomy
    taxonomy = generate_taxonomy(traits_data, 1, 2, 8)
    visualize_taxonomy(taxonomy, "../out/random_taxonomy.png")


if __name__ == "__main__":
    main()


"""
TODO:
- random seeds
- mark apex predators as territorial
"""
