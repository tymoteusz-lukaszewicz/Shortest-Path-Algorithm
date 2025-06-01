# Shortest-Path-Algorithm

# Ant Colony Optimization for Shortest Path Estimation

## Purpose

This project implements an estimation algorithm for finding a near-optimal solution to the Traveling Salesman Problem (TSP) using the principles of Ant Colony Optimization (ACO). It simulates the behavior of ants searching for the shortest path between a set of points.

This project was developed as a collaborative effort with [w0jtPL](https://github.com/w0jtPL).

## Key Features

* **Ant Colony Optimization:** Implements the ACO metaheuristic to iteratively improve the solution by simulating ant behavior.
* **Distance and Feromone-Based Path Selection:** Ants choose their paths based on a combination of the distance to the next node and the amount of feromone deposited on the edges.
* **Feromone Update:** Feromone levels on the paths are updated after each iteration, with shorter paths receiving more feromone.
* **Feromone Evaporation:** Feromone evaporates over time to avoid premature convergence to a suboptimal solution.
* **Visualization:** Uses Pygame to visualize the nodes, edges, feromone levels (represented by the intensity of green lines), and the best path found so far (blue line).

## Technologies Used

* Programming Language: Python
* Libraries:
    * NumPy: For efficient numerical operations.
    * Pygame: For visualization.
    * random: For random number generation.

## Algorithm Parameters

The algorithm's behavior is controlled by several key parameters:

* `FERO_SCALE`: Controls the amount of feromone deposited by ants.
* `EVAPORATION_RATE`: Determines how quickly feromone evaporates.
* `ALPHA`: Controls the influence of distance on path selection.
* `BETA`: Controls the influence of feromone on path selection.

## Setup Instructions

1.  Make sure you have Python 3.x installed.
2.  Install the required libraries:

    ```bash
    pip install numpy pygame
    ```

3.  Ensure that the `ants.py` file is in your working directory.

## Running the Code

To run the simulation, execute the `ants.py` script:

```bash
python ants.py
