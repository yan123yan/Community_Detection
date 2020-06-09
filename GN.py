import snap
import operator
import networkx as nx

#Girvan Newman method by Snap
def GirvanNewmanMethodBySnap(graph):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(graph, CmtyV)
    for Cmty in CmtyV:
        print("Community: ",CmtyV)
        # for NI in Cmty:
        #     print(NI)
    print("The modularity of the network is %f" % modularity)

# #Girvan Newman method by Networkx
# def GirvanNewmanMethodByNetworkx(G):
#     while 1:
#         print("The number of edges: ", len(G.edges()))
#         ebc = nx.centrality.edge_betweenness_centrality(G,normalized=False)
#         #print(ebc)
#         #print("节点编号及其边介数最大值为：")
#         ebc_list = sorted(ebc.items(), key=operator.itemgetter(1),reverse=True)
#         #print(ebc_list)
#         G.remove_edge(*ebc_list[0][0])

class GN:
    def __init__(self, G):
        self.G_copy = G.copy()
        self.G = G
        self.partition = [[n for n in G.nodes()]]
        self.all_Q = [0.0]
        self.max_Q = 0.0
        self.zidian = {0: [0]}

    # Using max_Q to divide communities
    def run(self):
        # Until there is no edge in the graph
        while len(self.G.edges()) != 0:
            # Find the most betweenness edge
            edge = max(nx.edge_betweenness_centrality(self.G).items(), key=lambda item: item[1])[0]
            # Remove the most betweenness edge
            self.G.remove_edge(edge[0], edge[1])
            # List the the connected nodes
            components = [list(c) for c in list(nx.connected_components(self.G))]
            if len(components) != len(self.partition):
                # compute the Q
                cur_Q = self.cal_Q(components, self.G_copy)
                if cur_Q not in self.all_Q:
                    self.all_Q.append(cur_Q)
                if cur_Q > self.max_Q:
                    self.max_Q = cur_Q
                    self.partition = components
                    for i in range(len(self.partition)):
                        self.zidian[i] = self.partition[i]
        print('-----------the Divided communities and the Max Q-----------')
        print('Max_Q:', self.max_Q)
        print('The number of Communites:', len(self.partition))
        print("Communites:", self.partition)
        return self.partition

    def cal_Q(self, partition, G):
        m = len(G.edges(None, False))
        a = []
        e = []
        for community in partition:
            t = 0.0
            for node in community:
                t += len([x for x in G.neighbors(node)])
            a.append(t / (2 * m))
        #             self.zidian[t/(2*m)]=community
        for community in partition:
            t = 0.0
            for i in range(len(community)):
                for j in range(len(community)):
                    if (G.has_edge(community[i], community[j])):
                        t += 1.0
            e.append(t / (2 * m))

        q = 0.0
        for ei, ai in zip(e, a):
            q += (ei - ai ** 2)
        return q

    def add_group(self):
        num = 0
        nodegroup = {}
        for partition in self.partition:
            for node in partition:
                nodegroup[node] = {'group': num}
            num = num + 1
        nx.set_node_attributes(self.G_copy, nodegroup)

    def to_gml(self):
        nx.write_gml(self.G_copy, 'outtoGN.gml')

def GirvanNewmanMethodByNetworkx(G):
    algorithm = GN(G)
    algorithm.run()
    algorithm.add_group()