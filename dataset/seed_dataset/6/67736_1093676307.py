import asyncio
@asyncio.coroutine
def main():
    p = yield from asyncio.create_subprocess_shell('echo hi')
    yield from p.wait()
asyncio.get_event_loop().run_until_complete(main())