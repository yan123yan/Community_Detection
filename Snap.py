import snap
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import networkx as nx
import operator
import igraph
from igraph import *
import community
from sympy import *
import math

#import HierarchicalClustering as HC
import SpectralClustering as SC
import CNM
import Infomap as IM
import FUCD
import GN
import HRG
import HC

import NMI


lj_path = r'F:\datasets\data_mining_network_communities\com-lj.ungraph.txt'
email_path = r'F:\datasets\data_mining_network_communities\data\email-Eu-core.txt'
DBLP_path = r'F:\datasets\data_mining_network_communities\com-dblp.ungraph.txt'

#np.set_printoptions(threshold=np.inf)

def load_data_by_snap(path,type='D'):
    if type == 'U':
        graph = snap.LoadEdgeList(snap.PUNGraph, path, 0 ,1)
    #snap.PrintInfo(graph, "python type PNGraph", "info-pngraph.txt", False)
    else:
        graph = snap.LoadEdgeList(snap.PNGraph, path, 0, 1)

    #节点数
    num_nodes = graph.GetNodes()
    print("The number of nodes: ",num_nodes)
    #边数
    num_edges = graph.GetEdges()
    print("The number of edges: ",num_edges)
    return graph

def load_data_by_networkx(path,type='D'):
    if type == 'U':
        graph = snap.LoadEdgeList(snap.PUNGraph, path, 0, 1)
        G = nx.Graph()

    elif type == 'HRG':
        graph = snap.LoadEdgeList(snap.PUNGraph, path, 0, 1)
        G = nx.Graph()

        for NI in graph.Nodes():
            G.add_node(NI.GetId())

        for EI in graph.Edges():
            if EI.GetSrcNId() != EI.GetDstNId():
                G.add_edge(EI.GetSrcNId(), EI.GetDstNId())

        return G

    else:
        graph = snap.LoadEdgeList(snap.PNGraph, path, 0, 1)
        G = nx.DiGraph()

    for NI in graph.Nodes():
        G.add_node(NI.GetId())

    for EI in graph.Edges():
        G.add_edge(EI.GetSrcNId(),EI.GetDstNId())
    # 节点数
    print("The number of nodes: ",len(G.nodes()))
    # 边数
    print("The number of edges: ",len(G.edges()))  #G.size()
    return G

def load_data_by_igraph(path,type='D'):

    if type == 'U':
        graph = snap.LoadEdgeList(snap.PUNGraph, path, 0, 1)
    else:
        graph = snap.LoadEdgeList(snap.PNGraph, path, 0, 1)

    vertex = []
    edges = []

    for NI in graph.Nodes():
        vertex.append(NI.GetId())

    for EI in graph.Edges():
        edges.append((EI.GetSrcNId(), EI.GetDstNId()))

    IG = igraph.Graph()
    #IG = igraph.Graph(n=len(vertex))
    IG.add_vertices(vertex)
    IG.add_edges(edges)

    # 节点数
    print("The number of nodes: ", len(vertex))
    # 边数
    print("The number of edges: ", len(edges))

    return IG, len(vertex)

#1.
def hierarchical_clustering():
    G = load_data_by_networkx(email_path, type='U')
    #HC.HierarchicalClustering(G,42)
    result = HC.HierarchicalClustering(G)
    return result

# 2. OK
def spectral_clustering():
    G = load_data_by_networkx(email_path, type='U')
    result = SC.SpectralClustering(G, cluster_num=42)
    return result

#3. OK
def cnm():
    IG, nums_node = load_data_by_igraph(email_path, type='U')
    result, clustering_nums = CNM.CNMAlgorithm(IG,nums_node)
    return result, clustering_nums

#4.
def hrg():
    G = load_data_by_networkx(email_path, type='U')
    T = nx.minimum_spanning_tree(G)
    E = set(T.edges())  # optimization
    print(E)
    NG = nx.Graph()
    NG.add_edges_from([e for e in G.edges() if e in E or reversed(e) in E])
    pos = HRG.hierarchy_pos(NG,1)
    nx.draw(G, pos=pos, with_labels=True)
    plt.savefig('hierarchy.png')


#5. OK
def infomap():
    IG, nums_node = load_data_by_igraph(email_path, type='U')
    result, clustering_nums = IM.InfomapAlgorithm(IG,nums_node)
    return result, clustering_nums

#6. OK
def fucd():
    G = load_data_by_networkx(email_path, type='U')
    result, clustering_nums = FUCD.FUCDAAlgorithm(G)
    return result, clustering_nums

#
def gn():
    G = load_data_by_networkx(email_path,type='U')
    GN.GirvanNewmanMethodByNetworkx(G)

#graph = load_data_by_snap(email_path,type='U')
#G = load_data_by_networkx(email_path)
#IG, nums_node = load_data_by_igraph(email_path,type='U')


#infomap_result, infomap_clustering_nums = infomap()
fucd_result, fucd_clustering_nums = fucd()
#cnm_result, cnm_clustering_nums = cnm()
# sc_result = spectral_clustering()
hc_result = hierarchical_clustering()
NMI.main(fucd_result,hc_result)


