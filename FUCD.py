import community

import networkx as nx


#6. Fast Unfolding community detection Algorithm
def FUCDAAlgorithm(G):
    partition = community.best_partition(G)
    print(partition)
    Q = community.modularity(partition,G)
    print("Q: ",Q)

    result = []

    for num in partition.keys():
        result.append(partition[num])

    print(set(partition.values()))
    clustering_nums = len(set(partition.values()))

    return result, clustering_nums

    #drawing
    # size = float(len(set(partition.values())))
    # pos = nx.spring_layout(G)
    # count = 0.
    # for com in set(partition.values()):
    #     count = count + 1.
    #     list_nodes = [nodes for nodes in partition.keys()
    #                   if partition[nodes] == com]
    #     nx.draw_networkx_nodes(G, pos, list_nodes, node_size=0.01,
    #                            node_color=str(count / size))

    #nx.draw_networkx_edges(G, pos, alpha=0.5)
    #plt.show()