import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import pandas as pd

G = nx.Graph()
R = np.matrix(np.zeros(shape=(5, 5)))
Q = np.matrix(np.zeros(shape=(5, 5)))


def construct_topo():
    edge = [
        (2, 3),
        (3, 2),
        (2, 1),
        (1, 2),
        (1, 5),
        (5, 1),
        (5, 4),
        (4, 5),
        (4, 3),
        (3, 4),
    ]  # *DYNAMIC
    edges = []
    for e in edge:
        edges.append((e[0] - 1, e[1] - 1))

    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()


def construct_reward_matrix():
    for key in G[4]:
        R[
            key, 4
        ] = 100  # NEED TO CALCULATE REWARD FOR EVERY LINK DYNAMICALLY, VIA INPUTS FROM PYGNMI
        print(R)


def construct_q_matrix():
    Q -= 100
    for node in G.nodes:
        for x in G[node]:
            Q[node - 1, x - 1] = 0
            Q[x - 1, node - 1] = 0
    pd.DataFrame(Q)  # Printing the Q Matrix


"""
Takes a node and returns the next node 
a) On the basis of the highest Q value for moving from s to s'
b) Randomly choosing the next node from the available connected nodes
"""


def nextNode(
    start, exp_rate
):  # exp_rate -> exploration rate (higher exp_rate = more probability of choosing a random node)
    random_value = random.uniform(0, 1)

    if (
        random_value < exp_rate
    ):  # if random_value is lower than exp_rate, choose the next node randomly
        sample = G[start]
    else:
        sample = np.where(Q[start,] == np.max(Q[start,]))[
            1
        ]  # finds index of the highest Q-Value in "start"'s row
    next_node = int(np.random.choice(sample, 1))
    return next_node


"""
Updating the Q values for the action taken
"""


def updateQ(node1, node2, alpha, gamma):  # alpha: learning rate, gamma: discount factor
    max_index = np.where(Q[node2,] == np.max(Q[node2,]))[
        1
    ]  # finds index of the highest Q-Value in that row
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[node2, max_index]
    Q[node1, node2] = int(
        Q[node1, node2]
        + alpha * (R[node1, node2] + gamma * max_value - Q[node1, node2])
    )


def learn(exp_rate, alpha, gamma):
    for i in range(50000):  # UPDATE THE SIZE OF THE WALK HERE
        start = np.random.randint(0, 5)  # UPPER LIMIT -> DYNAMIC
        next_node = nextNode(start, exp_rate)
        updateQ(start, next_node, alpha, gamma)


def shortest_path(begin, end):
    path = [begin]
    next_node = np.argmax(
        Q[
            begin,
        ]
    )
    path.append(next_node)
    while next_node != end:
        next_node = np.argmax(
            Q[
                next_node,
            ]
        )
        path.append(next_node)
    return path


if __name__ == "__main__":
    construct_topo()
    learn(0.9, 0.81, 0.96)  # INCLUDE IT IN A FUNCTION
    shortest_path(2, 4)
