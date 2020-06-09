import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt

def similarity_matrix(G,node_nums,node_list):
    similarity_matrix = np.zeros((node_nums, node_nums))
    for first_node_index in range(len(node_list)):
        for second_node_index in range(len(node_list)):

            if first_node_index == second_node_index:
                continue

            first_node = node_list[first_node_index]
            second_node = node_list[second_node_index]
            first_neighbor_nodes = G.neighbors(first_node)
            second_neighbor_nodes = G.neighbors(second_node)
            first_node_set = set()
            second_node_set = set()
            for f in first_neighbor_nodes:
                first_node_set.add(f)
            for s in second_neighbor_nodes:
                second_node_set.add(s)
            Jaccard = len(first_node_set & second_node_set) / len(first_node_set | second_node_set)
            similarity_matrix[first_node_index, second_node_index] = Jaccard
    # print(similarity_matrix)
    return similarity_matrix

def Wmatrix(G,node_nums,node_list):
    w_matrix = np.zeros((node_nums, node_nums))
    for first_node_index in range(len(node_list)):
        for second_node_index in range(len(node_list)):
            if first_node_index == second_node_index:
                continue

            first_node = node_list[first_node_index]
            second_node = node_list[second_node_index]
            first_neighbor_nodes = G.neighbors(first_node)

            if second_node in first_neighbor_nodes:
                w_matrix[first_node_index, second_node_index] = 1
    return w_matrix

#average  1.5:35:0.18,1.6:25:0.197,1.7:17:0.257,1.8:13:0.286
#centroid ,1.3:26:0.273,1.4:22:0.282,1.5:11:0.251,
def h(data, method='average', threshold=1.8):
    Z = linkage(data, method=method)
    cluster_assignments = fcluster(Z, threshold, criterion='distance')
    print(type(cluster_assignments))
    num_clusters = max(cluster_assignments)
    indices = get_cluster_indices(cluster_assignments)
    dn = dendrogram(Z)
    plt.show()

    return num_clusters, indices


def get_cluster_indices(cluster_assignments):
    '''映射每一类至原数据索引

    Arguments:
        cluster_assignments 层次聚类后的结果

    Returns:
        [[idx1, idx2,..], [idx3]] -- 每一类下的索引
    '''
    n = cluster_assignments.max()
    indices = []
    for cluster_number in range(1, n + 1):
        indices.append(np.where(cluster_assignments == cluster_number)[0])

    return indices

def node_degree(node,array):
    #计算节点的度数
    degree =sum(array[node])
    return degree

def A(i,j,array):
    #判断两个节点是否存在边
    if array[i,j]==0:
        return 0
    else:
        return 1

def k(i,j,array):
    #计算两个节点的度数积
    kij = node_degree(i,array) *node_degree(j,array)
    return kij

def judge_cluster(i,j,l):
    #判断两个节点是否在一个社区
    if l[i] == l[j]:
        return 1
    else:
        return 0

def Q(array, cluster):
    q = 0
    m = sum(sum(array)) / 2  # 总边数
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
            if judge_cluster(i, j, cluster) != 0:
                q += (A(i, j, array) - (k(i, j, array) / (2 * m))) * judge_cluster(i, j, cluster)
    q = q / (2 * m)
    print("Q: ",q)
    return q

def HierarchicalClustering(G):
    #从底向上
    node_nums = len(G.nodes())
    node_list = list(G.nodes())

    # target_list = []
    # for node in node_list:
    #     target_list.append([node])

    #print(target_list)

    M = similarity_matrix(G,node_nums,node_list)
    r, c = M.shape
    for i in range(r):
        for j in range(i,c):
            if M[i,j] != M[j,i]:
                M[i,j] = M[j,i]

    num_clusters, indices = h(M)
    print("%d clusters" % num_clusters)

    result = [0 for n in range(node_nums)]

    for k, ind in enumerate(indices):
        print("cluster", k + 1, "is", ind)
        for each in ind:
            result[each] = k

    #print(result)
    W = Wmatrix(G,node_nums,node_list)
    Q(W,result)
    return result