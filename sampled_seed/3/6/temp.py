import numpy as np
import multiprocessing
import _tkinter

def parallel_matmul(x):
    x = np.random.randn(3, 3)
    return np.matmul(x, x)
pool = multiprocessing.Pool(4)
results = pool.map(pool, [np.random.randn(3, 5000) for pool in range(2)])