
#Infomap Algorithm
#U
def InfomapAlgorithm(IG, nums_node):
    community = IG.community_infomap()
    community_list = []
    for each_item in community:
        community_list.append(each_item)
    membership = []
    for i in range(0, nums_node):
        membership.append(0)
    for j in range(0, len(community_list)):
        nodes = community_list[j]
        for k in nodes:
            membership[k] = j
    Q = community.modularity
    print("Q: ",Q)

    #获得聚类个数
    clustering_nums = len(community)

    #创建全为0的列表，长度为nums_node
    result = [0 for n in range(nums_node)]
    #print(str(len(result)))

    for index in range(len(community)):
        each_list =  community[index]
        for e in each_list:
            result[e] = index
    #print(community)
    print(result)

    return result, clustering_nums