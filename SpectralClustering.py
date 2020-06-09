import numpy as np
from sklearn.cluster import KMeans
import random
import matplotlib.pyplot as plt
import pandas as pd
import scipy.linalg as linalg
from numpy import *
import networkx as nx
from scipy import cluster

#Spectral Clustering
#References: https://www.cnblogs.com/pinard/p/6221564.html

#..
def SpectralClustering(G,cluster_num):
    #G networkx
    node_list = list(G.nodes())
    node_nums = len(G.nodes())

    adjacency_matrix = np.zeros((node_nums,node_nums),dtype='i')
    for first_node_index in range(len(node_list)):

        first_node = node_list[first_node_index]
        first_neighbor_node = G.neighbors(first_node)
        for node in first_neighbor_node:
            if first_node == node:
                continue
            adjacency_matrix[first_node,node] = 1

    print(adjacency_matrix)

    degree_matrix = np.zeros((node_nums,node_nums))
    for node_index in range(len(node_list)):
        _node = node_list[node_index]
        neighbor_nodes = G.neighbors(_node)
        nums = 0
        for i in neighbor_nodes:
            nums = nums + 1
        degree_matrix[_node,_node] = nums

    laplacian_matrix = degree_matrix - adjacency_matrix

    #标准化
    sqrtDegreeMatrix = np.power(np.linalg.matrix_power(degree_matrix,-1),0.5)
    normalize_laplacian_matrix = sqrtDegreeMatrix @ laplacian_matrix @ sqrtDegreeMatrix
    normalize_laplacian_matrix[normalize_laplacian_matrix == -1] = 0.0
    #print("bbbbb>>>>>>",normalize_laplacian_matrix)

    #特征值分解
    eig_lambda,eig_vector = linalg.eig(normalize_laplacian_matrix)
    #返回第二小的特征值对应的下标,根据下标找到对应的特征向量
    x = eig_vector[:,np.argsort(eig_lambda)[0:cluster_num]]
    #print(x)

    clustering = KMeans(n_clusters=cluster_num)
    clustering.fit(np.real(x))
    label_pred = clustering.labels_ #获取聚类标签
    centroids = clustering.cluster_centers_  # 获取聚类中心
    inertia = clustering.inertia_  # 获取聚类准则的总和
    #print(inertia)

    return label_pred
