import numpy as np

class vars():
    def __init__(self):
        self.n_default = 100000
        self.n_ls = 1000*np.array([1,2,5,10,20,50,100,200,500])
        self.p_ls = np.array([0.01, 0.02, 0.05, 0.1, 0.2, 0.5])