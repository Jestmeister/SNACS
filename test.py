import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from artificial_data import get_degree_dist
from cada import cada
from sklearn.metrics import f1_score

n_default = 100000
n_ls = 1000*np.array([1,2,5,10,20,50,100,200,500])
p_ls = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
n_inj = int(n_default/100)
path = f"art_data/artdat-p{0.2}.txt"
pr_graph = nx.read_adjlist(path,nodetype=int)

ground_truth = np.zeros(len(pr_graph),dtype=int)
ground_truth[n_default:] = 1
#print(sum(ground_truth))
#va fan e felet...
cada_lv = cada(pr_graph)
pred = cada_lv.clf(n_inj)
print(f1_score(ground_truth,pred))