import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from artificial_data import get_degree_dist
from cada import cada
from sklearn.metrics import f1_score,recall_score,precision_score
import community
from networkx.algorithms.community import greedy_modularity_communities as gmc
import igraph as ig
import leidenalg

def test():
    n_default = 100000
    #n_default = 1000
    n_ls = 1000*np.array([1,2,5,10,20,50,100,200,500])
    p_ls = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
    n_inj = int(n_default/100)
    path = f"art_data/artdat-p0.2.txt"
    #path = f"art_data/artdat-n1000.txt"
    pr_graph = nx.read_adjlist(path,nodetype=int)


    ground_truth = np.zeros(len(pr_graph),dtype=int)
    ground_truth[n_default:] = 1
    #cadar = cada(pr_graph,algorithm='greedy',resolution=6)
    cadar = cada(pr_graph,algorithm='fluid')
    #cadar = cada(pr_graph,algorithm='leiden')
    #cadar = cada(pr_graph,algorithm='louvain')
    pred = cadar.clf(n_inj)
    print(f1_score(ground_truth,pred))
    print(precision_score(ground_truth,pred))
    print(recall_score(ground_truth,pred))
    #a = pred - ground_truth
    #b = len(a[a==0])
    #print(b)
    #something wrong w f1-score??
    #apan = community.best_partition(pr_graph, resolution=0.1)
    #it = nx.algorithms.community.asyn_fluidc(pr_graph,2)
    #make so async returns a dict with key: node, val: community

    #greedy scales like a donkey...

test()