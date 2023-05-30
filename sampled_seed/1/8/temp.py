import asyncio
import socket

def receiver(loop):
    (a, b) = socket.socketpair()
    loop.call_later(1, lambda : print('Should be called inside the loop'))
    end = loop.time() + 3
    print('Starting busy receiver')
    while loop.time() < end:
        a.send(b'test')
        yield from loop.sock_recv(end, 65536)
    print('Busy receiver complete')
    yield from asyncio.sleep(0.5)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(receiver(loop))
    loop.close()
if __name__ == '__main__':
    main()