import asyncio
import threading
fut = asyncio.Future()

async def coro(loop):
    fut.add_done_callback(lambda _: loop.stop())
    loop.call_later(1, fut.set_result, None)
    while True:
        await asyncio.sleep(100000)

def run():
    fut = asyncio.new_event_loop()
    asyncio.set_event_loop(fut)
    loop.run_until_complete(coro(fut))
    loop.close()
run = threading.Thread(target=run)
t.start()
t.join()