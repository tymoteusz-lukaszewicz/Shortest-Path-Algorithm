import numpy as np
import pygame as pg
import random


FERO_SCALE = 1          # Feromone scale
EVAPORATION_RATE = 0.1  # Feromone evaporation rate
ALPHA = 1.5             # Distance influence
BETA = 2.5              # Feromone influence
NUMBER_OF_POINTS = 20   # Number of points to simulate


def cdist(XA, XB):
    XA = np.asarray(XA)
    XB = np.asarray(XB)

    # Efficient vectorized formula: ||a - b||^2 = ||a||^2 + ||b||^2 - 2 * a.b
    XA_sq = np.sum(XA**2, axis=1, keepdims=True)  # shape (mA, 1)
    XB_sq = np.sum(XB**2, axis=1, keepdims=True).T  # shape (1, mB)
    cross_term = np.dot(XA, XB.T)  # shape (mA, mB)

    dists_squared = XA_sq + XB_sq - 2 * cross_term
    # Ensure numerical stability (no negative small numbers due to float errors)
    np.maximum(dists_squared, 0, out=dists_squared)

    return np.sqrt(dists_squared)


def weight_from_dist_and_fero(dist, fero, alpha, beta):
    '''Calculates path weight'''
    return (1/dist)**alpha+fero**beta


def lerp(x, a, b, c, d):
    """Linear interpolation."""
    return (c + (x - a) * (d - c) / (b - a) if b != a else (c+d)/2)

class Ant:
    """Ant agent."""
    def __init__(self, nodes: list[int], fero_weights):
        self.nodes_to_visit = nodes      # nodes to visit
        self.fero_weights = fero_weights # feromone matrix
        self.cost = 0                    # overall cost of ant's path
        self.path = []                   # path

    def go_antie_go(self):
        cur_node = self.nodes_to_visit.pop(random.randint(0, len(self.nodes_to_visit)-1)) # start node
        self.path.append(cur_node)
        while self.nodes_to_visit:
            cur_node = self.nodes_to_visit.pop(random.choices(range(len(self.nodes_to_visit)), weights=[weight_from_dist_and_fero(weights[cur_node, i],
                                                                                                                                  self.fero_weights[cur_node, i],
                                                                                                                                  ALPHA, BETA)
                                                                                                         for i in self.nodes_to_visit])[0])    # next node
            self.path.append(cur_node)
        self.cost = sum([weights[self.path[i-1], self.path[i]] for i in range(len(self.path))]) # path cost
    
    def update_fero_weights(self):
        """Update feromone on path."""
        for i in range(1, len(self.path)):
            a, b = self.path[i - 1], self.path[i]
            self.fero_weights[a, b] += FERO_SCALE / self.cost  # add feromone
            self.fero_weights[b, a] += FERO_SCALE / self.cost



pg.init()

size = 500

nodes = np.random.rand(20, 2)*(size-100)+50 # random nodes
display = pg.display.set_mode((size, size))
clock = pg.time.Clock()

weights = cdist(nodes, nodes) # distance matrix
fero_weights = np.zeros_like(weights) # feromone matrix

run = True
best_ant = ...
best_cost = float('inf')
while run:
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            run = False
    
    display.fill('black')

    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i==j:
                continue
            else:
                list_of_weights = fero_weights.flatten()
                mini = list_of_weights.min()
                maxi = list_of_weights.max()
                pg.draw.line(display, (0, lerp(fero_weights[i, j], mini, maxi, 0, 255), 0), nodes[i], nodes[j]) # draw feromone
                
    

    for n in nodes:
        pg.draw.circle(display, 'red', n, 5) # draw nodes
    
    population = 1000 # ant population per epoch
    ants = [Ant(list(range(len(nodes))), fero_weights) for _ in range(population)] # create ants agents
    for ant in ants:
        ant.go_antie_go() # ant finds path
        if ant.cost < best_cost: # update best path
            best_cost = ant.cost
            best_ant = ant
    fero_weights *= EVAPORATION_RATE # feromone evaporation
    for ant in ants:
        ant.update_fero_weights() # ant updates feromone

    for i in range(len(best_ant.path)):
        pg.draw.line(display, "blue", nodes[best_ant.path[i]], nodes[best_ant.path[i-1]], 3) # draw best path in blue

    pg.display.flip()