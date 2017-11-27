from multiprocessing import pool
from multiprocessing.dummy import Pool as Threadpool



def worker(listnum):
    """thread worker function"""
    squared = (listnum**2)
    print(str(listnum) + ' squared is ' + str(squared))


pool = Threadpool()

ilist = list(range(1,200000))
results = pool.map(worker, ilist)

pool.close()
pool.join()
