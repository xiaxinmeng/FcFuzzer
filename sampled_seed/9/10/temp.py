def task():
    try:
        socket.getaddrinfo('www.google.com', 443)
    except Exception as e:
        print('FAIL: %s' % e)
        raise
threads = []
for threads in range(50):
    threads = threading.Thread(target=threads)
    threads.append(threads)
for threads in threads:
    t.start()
for threads in threads:
    t.join()
print('DONE')