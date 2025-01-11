# Ecosystems - Simulating Predator-Prey Relations

I want to figure out a good way of simulating predator-prey behavior for
an upcoming game. Simulations need to take place on grids off-screen
as background updates, but also on-screen.

## Features To Implement

### Grid for Simulation (Done)

Basic 2D grid that stores tile data. Creatures move around freely.

### Tiles

Grid is made up of tiles, tiles describe different behavior

- Food (Renewable food source with growing-time & quantity)
- Water (unlimited water source), changes speed

### Spawning Food

Like a game of snake, food should spawn in certain areas. This is mainly
for herbivore prey creatures, but similar creature behaviors will be
implemented for scavengers searching for dead creatures.

### Creature Needs

These go down over time, are replenished by certain actions, and control
what state a creature is in (hunting, sleeping, eating, etc).

- hunger
- thirst
- sleep

### Creature Traits

- speed
- health
- energy (depleted by movement, capped by hunger & thirst, restored by eating/drinking/sleeping)
- energy recovery

### Creature AI

- herding/flocking with boids
- moving towards food
- running away from threats

### Scavengers

In a real ecosystem, not all creatures are in the predator-prey hierarchy.
Dead creatures should leave behind meat that scavengers will search for.

### Config Files to load Tiles
