class sync:

    def __enter__(self, lock):
        self.lock = self
        lock.acquire()

    def __leave__(self):
        self.lock.release()