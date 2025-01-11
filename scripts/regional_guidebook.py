# Create a region-divided guidebook that uses the affinity-splitting system
# to determine creature evolutions pseudo-realistically (at least realistic
# in the game)
# RULES:
# - Each region has certain allowed affinities based on geographic features
# - Most creature families can appear in most regions, but are then linked
# to a primary affinity. The design should answer the questions, "What drove
# this creature to evolve to live here; why does it live here now?"
# - Creatures can be predators or prey creatures (affecting their AI in the
# game), which should be taken into account when designing regions
# - Each region is its own ecosystem, but it is not closed. Creatures can
# move between regions, for example, a certain seacrab may normally be on
# the beach but will travel to the cliffs when it rains because that's also
# when one of its predators comes out of the jungle and onto the beach.
# Small discoveries like this will help make the game feel alive, sell the
# realism, engage the player, and remind them that they are a part of this
# ecosystem now.
import json

import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
from typing import Dict, List, Tuple

from ecosystems.generation.creature import Creature
from ecosystems.generation.region import Region, get_region_affinities, add_region_affinities
from ecosystems.generation.probability import generate_from_list, generate_potential_pair, weighted_randint


def simple_island_regions(region_affinities: Dict) -> nx.MultiDiGraph:
    # Create a simple MultiDiGraph connecting up a concept of the island
    # to visualize connectivity (../res/simple_island.png)
    island = nx.MultiDiGraph()
    # Create all the regions first, adding extra affinities for mixed
    # regions as necessary
    # Base regions
    beach = Region("Beach", "Beach",
                   get_region_affinities(region_affinities, "Beach"))
    cliffs = Region("Cliffs", "Cliffs",
                    get_region_affinities(region_affinities, "Cliffs"))
    jungle = Region("Jungle", "Jungle",
                    get_region_affinities(region_affinities, "Jungle"))
    meadow = Region("Meadow", "Meadow",
                    get_region_affinities(region_affinities, "Meadow"))
    swamp = Region("Swamp", "Swamp",
                   get_region_affinities(region_affinities, "Swamp"))
    desert = Region("Desert", "Desert",
                    get_region_affinities(region_affinities, "Desert"))
    volcano = Region("Volcano", "Volcano",
                     get_region_affinities(region_affinities, "Volcano"))
    tundra = Region("Tundra", "Tundra",
                    get_region_affinities(region_affinities, "Tundra"))
    glacier = Region("Glacier", "Glacier",
                     get_region_affinities(region_affinities, "Glacier"))
    cave = Region("Cave", "Cave",
                  get_region_affinities(region_affinities, "Cave"))

    # Specific / Combined regions
    starting_beach = Region.from_region(beach, name="Starting Beach")
    haunted_jungle = Region.from_region(jungle, name="Haunted Jungle")
    open_meadow = Region.from_region(meadow, name="Open Meadow")
    toxic_swamp = Region.from_region(swamp, name="Toxic Swamp")
    lush_cliffs = Region("Lush Cliffs", "Cliffs",
                         add_region_affinities(jungle, cliffs))
    frozen_jungle = Region("Frozen Jungle", "Jungle",
                           add_region_affinities(jungle, glacier))
    frozen_marsh = Region("Frozen Marsh", "Swamp",
                          add_region_affinities(swamp, glacier))
    brackish_beach = Region("Brackish Beach", "Beach",
                            add_region_affinities(beach, swamp))
    volcanic_swamp = Region("Volcanic Swamp", "Swamp",
                            add_region_affinities(volcano, swamp))
    volcanic_beach = Region("Volcanic Beach", "Beach",
                            add_region_affinities(volcano, beach))
    volcanic_cliffs = Region("Volcanic Cliffs", "Cliffs",
                             add_region_affinities(volcano, cliffs))
    frosty_desert = Region("Frosty Desert", "Desert",
                           add_region_affinities(tundra, desert))
    barren_desert = Region.from_region(desert, name="Barren Desert")
    muddy_mire = Region("Muddy Mire", "Swamp",
                        add_region_affinities(swamp, desert))
    glacial_peak = Region.from_region(glacier, name="Glacial Peak")
    sparse_tundra = Region.from_region(tundra, name="Sparse Tundra")
    steep_cliffs = Region.from_region(cliffs, name="Steep Cliffs")

    # Connect up the graph
    # Two-way
    island.add_edges_from([
        # Starting Beach
        (starting_beach, haunted_jungle), (haunted_jungle, starting_beach),
        (starting_beach, open_meadow), (open_meadow, starting_beach),
        (starting_beach, lush_cliffs), (lush_cliffs, starting_beach),
        (starting_beach, brackish_beach), (brackish_beach, starting_beach),
        # Haunted Jungle
        (haunted_jungle, lush_cliffs), (lush_cliffs, haunted_jungle),
        (haunted_jungle, sparse_tundra), (sparse_tundra, haunted_jungle),
        (haunted_jungle, frozen_jungle), (frozen_jungle, haunted_jungle),
        (haunted_jungle, frozen_marsh), (frozen_marsh, haunted_jungle),
        (haunted_jungle, open_meadow), (haunted_jungle, open_meadow),
        # Open Meadow
        (open_meadow, frozen_jungle), (frozen_jungle, open_meadow),
        (open_meadow, frozen_marsh), (frozen_marsh, open_meadow),
        (open_meadow, toxic_swamp), (toxic_swamp, open_meadow),
        # Lush Cliffs
        (lush_cliffs, steep_cliffs), (steep_cliffs, lush_cliffs),
        (lush_cliffs, sparse_tundra), (sparse_tundra, lush_cliffs),
        # Brackish Beach
        (brackish_beach, toxic_swamp), (toxic_swamp, brackish_beach),
        (brackish_beach, volcanic_swamp), (volcanic_swamp, brackish_beach),
        (brackish_beach, volcanic_beach), (volcanic_beach, brackish_beach),
        # Sparse Tundra
        (sparse_tundra, steep_cliffs), (steep_cliffs, sparse_tundra),
        (sparse_tundra, frozen_jungle), (frozen_jungle, sparse_tundra),
        (sparse_tundra, glacial_peak), (glacial_peak, sparse_tundra),
        (sparse_tundra, frosty_desert), (frosty_desert, sparse_tundra),
        (sparse_tundra, frozen_marsh), (frozen_marsh, sparse_tundra),
        # Frozen Jungle
        (frozen_jungle, frozen_marsh), (frozen_marsh, frozen_jungle),
        # Frozen Marsh
        (frozen_marsh, toxic_swamp), (toxic_swamp, frozen_marsh),
        (frozen_marsh, frosty_desert), (frosty_desert, frozen_marsh),
        # Toxic Swamp
        (toxic_swamp, muddy_mire), (muddy_mire, toxic_swamp),
        (toxic_swamp, volcanic_swamp), (volcanic_swamp, toxic_swamp),
        # Steep Cliffs
        (steep_cliffs, frosty_desert), (frosty_desert, steep_cliffs),
        (steep_cliffs, volcanic_cliffs), (volcanic_cliffs, steep_cliffs),
        # Volcanic Swamp
        (volcanic_swamp, muddy_mire), (muddy_mire, volcanic_swamp),
        (volcanic_swamp, volcanic_beach), (volcanic_beach, volcanic_swamp),
        # Volcanic Beach
        (volcanic_beach, barren_desert), (barren_desert, volcanic_beach),
        (volcanic_beach, volcanic_cliffs), (volcanic_cliffs, volcanic_beach),
        # Glacial Peak
        # Frosty Desert
        (frosty_desert, barren_desert), (barren_desert, frosty_desert),
        # Muddy Mire
        (muddy_mire, barren_desert), (barren_desert, muddy_mire),
        # Barren Desert
        (barren_desert, volcanic_cliffs), (volcanic_cliffs, barren_desert)
        # Volcanic Cliffs
    ])

    # One-way
    island.add_edges_from([
        (glacial_peak, frozen_jungle),
        (glacial_peak, frozen_marsh)
    ])

    return island


def viz_graph(G: nx.MultiDiGraph, filename: str):
    A = nx.nx_agraph.to_agraph(G)
    A.layout("dot")
    A.graph_attr.update(size='10,10!')
    A.graph_attr.update(dpi='300')
    A.graph_attr.update(ratio='1')

    A.draw(filename)


def region_food_web(region: Region, num_creatures: int,
                    prey_creature_family: List[str],
                    middle_creature_family: List[str],
                    apex_creature_family: List[str]) -> Tuple[Dict, nx.MultiDiGraph]:
    # Generate creatures based on the region's affinities, then create a
    # graph showing the predator-prey relations
    # Rules:
    # 30% of creatures are herbivore prey animals
    # 50% of creatures are omnivorous middle-of-the-pack animals
    # 20% of creatures are apex predators
    possible_affinities = region.affinities
    num_prey = num_creatures // 3
    num_middle = num_creatures // 2
    num_apex = num_creatures - num_middle - num_prey
    creatures = {"Prey": [], "Middle": [], "Apex": []}
    food_web = nx.MultiDiGraph()  # predator -> prey
    # Create prey
    for i in range(num_prey):
        affinities = [random.choice(possible_affinities), ""]  # 1 affinity
        family = random.choice(prey_creature_family)
        prey_creature = Creature(affinities, family, "Random", f"Prey_{i}")

        creatures["Prey"].append(prey_creature)
        food_web.add_node(prey_creature)

    # Create middle
    for i in range(num_middle):
        affinities = generate_potential_pair(possible_affinities,
                                             0.25)  # 1 or 2 affinities
        family = random.choice(middle_creature_family)
        middle_creature = Creature(affinities, family, "Random", f"Middle_{i}")
        creatures["Middle"].append(middle_creature)
        # Pick at least 1 prey creature this creature hunts
        hunted_prey = random.sample(creatures["Prey"],
                                    weighted_randint(1, num_prey))
        for j, prey in enumerate(hunted_prey):
            food_web.add_edge(middle_creature, prey,
                              hunter=middle_creature.name)  # predator -> prey

            middle_creature.prey.append(prey)
            prey.predators.append(middle_creature)

    # Create apex predators
    for i in range(num_apex):
        affinities = generate_potential_pair(possible_affinities,
                                             0.75)  # 1 or 2 affinities
        family = random.choice(apex_creature_family)
        apex_creature = Creature(affinities, family, "Random", f"Apex_{i}")
        creatures["Apex"].append(apex_creature)
        # Pick prey and middle creatures this creature hunts
        hunted_prey = random.sample(creatures["Prey"],
                                    random.randint(1, num_prey)) +\
            random.sample(creatures["Middle"],
                          random.randint(1, num_middle))
        for j, prey in enumerate(hunted_prey):
            food_web.add_edge(apex_creature, prey,
                              hunter=apex_creature.name)  # predator -> prey

            apex_creature.prey.append(prey)
            prey.predators.append(apex_creature)

    return creatures, food_web


def main():
    # Load data
    with open("../res/region_affinities.json", "r", encoding="utf-8") as infile:
        region_affinities = json.load(infile)

    with open("../res/creature_traits.json", "r", encoding="utf-8") as infile:
        creature_traits = json.load(infile)

    island = simple_island_regions(region_affinities)
    # View (just for sanity)
    # visualize_island_regions(island, "../out/simple_island.png")
    # Test with meadow

    creatures, food_web = region_food_web(
        Region("Meadow", "Meadow", get_region_affinities(region_affinities,
                                                         "Meadow")),
        10,
        ["Cow-like", "Rabbit-like", "Rodent-like"],
        ["Lizard-like", "Snake-like", "Feline"],
        ["Crocodilian", "Canine"])

    # print(creatures)
    viz_graph(food_web, "../out/meadow_food_web.png")


if __name__ == "__main__":
    main()


# TODO:
# - Make library & Git repo!
# - Generate creatures based on region affinities
# - Simulate predator-prey, herding/flocking & travelling for single region ecosystem
#   - Make M x N size grid
#   - Populate with regenerating food nodes
#   - Simple AI to try to find food
# - Simulate travel across boundaries
# - Add weather, day/night
# - separate out hunters, foragers, scavengers, or create scavengers as a
#   separate set of entities
