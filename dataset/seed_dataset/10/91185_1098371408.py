def main():
    q = multiprocessing.Queue()
    q.put(0)
    #time.sleep(0.001) # Issue goes away when this line is uncommented
    q.close()
    q.join_thread()