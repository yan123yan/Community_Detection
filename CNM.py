import igraph

#CNM Algorithm
#U
def CNMAlgorithm(IG, nums_node):
    H = IG.community_fastgreedy(weights=None)
    c = list(H.as_clustering())

    membership = []
    for i in range(0, nums_node):
        membership.append(0)
    # 根据社团划分对membership赋值
    for i in range(0, len(c)):
        nodes = c[i]
        for j in nodes:
            membership[j] = i
    #根据membership计算模块度
    Q = igraph.GraphBase.modularity(IG, membership)
    print("Q: ",Q)

    # 获得聚类个数
    clustering_nums = len(c)
    #print(clustering_nums)

    # 创建全为0的列表，长度为nums_node
    result = [0 for n in range(nums_node)]
    # print(str(len(result)))

    for index in range(len(c)):
        each_list = c[index]
        for e in each_list:
            result[e] = index
    # print(community)
    print(result)

    return result, clustering_nums