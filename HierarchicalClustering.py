import networkx as nx
import numpy as np

def HierarchicalClustering(G,k):
    #print(G.nodes)
    node_nums = len(G.nodes())
    node_list = list(G.nodes)
    #print(node_list)
    while len(node_list) >= k:
        print("node 个数为：",str(len(node_list)))
        min = 10
        r = 0
        c = 0
        for node in range(len(node_list)-1):
            node0 = node_list[node]
            node1 = node_list[node+1]
            if isinstance(type(node0),list) and isinstance(type(node1),list):
                #是一个列表
                new_set1 = set()
                for each1 in node1:
                    new_set1.add(x for x in list(G.neighbors(each1)))
                new_set0 = set()
                for each0 in node0:
                    new_set0.add(x for x in list(G.neighbors(each0)))

                S = JaccardSimilarity(new_set1,new_set0)
            elif isinstance(type(node1),list):
                #是一个列表
                new_set = set()
                for each in node1:
                    new_set.add(x for x in list(G.neighbors(each)))
                node0_set = set(x for x in list(G.neighbors(node0)))
                S = JaccardSimilarity(new_set, node0_set)
            elif isinstance(type(node0),list):
                #是一个列表
                new_set = set()
                for each in node0:
                    new_set.add(x for x in list(G.neighbors(each)))
                node1_set = set(x for x in list(G.neighbors(node1)))
                S = JaccardSimilarity(new_set, node1_set)
            else:
                if node0 != node1:
                    #print(G.neighbors(node0))
                    node0_set = set()
                    for i in list(G.neighbors(node0)):
                        node0_set.add(i)
                    node1_set = set()
                    for j in list(G.neighbors(node1)):
                        #print(type(j))
                        node1_set.add(j)
                    S = JaccardSimilarity(node0_set,node1_set)
                else:
                    S = 0.0

            if S != 0.0 and S < min:
                min = S
                r, c = node0,node1
        node_list.remove(r)
        node_list.remove(c)
        node_list.append([r,c])

def indmin_matrix(M):
    '''得到矩阵M中最小元素的行列坐标'''
    row,col = divmod(np.argmin(M), np.shape(M)[1])
    return row,col

def JaccardSimilarity(set1,set2):
    Jaccard_similarity = len(set1 & set2) / len(set1 | set2)
    return Jaccard_similarity