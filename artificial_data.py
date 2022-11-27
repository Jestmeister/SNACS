import networkx as nx
import numpy as np

#Parameters
n_default = 100000
p_default = 0.2
n_ls = 1000*np.array([1,2,5,10,20,50,100,200,500])
p_ls = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

def get_degree_dist(G):
    # G is undirected
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    vals, counts=np.unique(degree_sequence, return_counts=True)
    return vals, counts
    

def inject_anomalies(n_anomalies, n, graph):
    # Injected nodes can connect to each other
    # First n nodes are "true"
    # The rest are "false"
    vals, count = get_degree_dist(graph)
    degree_dist = count/sum(count)
    for i in range(n_anomalies):
        graph.add_node(n+i)
        n_connections = np.random.choice(vals, p=degree_dist)
        connecting_nodes = np.random.permutation(n+i)
        conncting_nodes = connecting_nodes[:n_connections]
        new_edges = [(n+i,node) for node in conncting_nodes]
        graph.add_edges_from(new_edges)
    return graph

if __name__=='__main__':
    #probability run
    for p in p_ls:
        print(f"Running probability {p}\n")
        #Parameters
        k = int(2*np.power(n_default,0.15))
        n_anomalies = int(n_default/100)
        path = f"art_data/artdat-p{p}.txt"

        #Generate artificial data
        ws_graph = nx.newman_watts_strogatz_graph(n=n_default,k=k,p=p)

        #intorduce anomalies
        anomaly_graph = inject_anomalies(n_anomalies, n_default, ws_graph)

        #Save data    
        nx.write_adjlist(anomaly_graph,path)

    #node run
    for n in n_ls:
        print(f"Running nodes {n}\n")
        #Parameters
        k = int(2*np.power(n,0.15))
        n_anomalies = int(n/100)
        path = f"art_data/artdat-n{n}.txt"

        #Generate artificial data
        ws_graph = nx.newman_watts_strogatz_graph(n=n,k=k,p=p_default)

        #intorduce anomalies
        anomaly_graph = inject_anomalies(n_anomalies, n, ws_graph)

        #Save data    
        nx.write_adjlist(anomaly_graph,path)