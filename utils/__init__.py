import asyncio
loop = asyncio.get_event_loop()
def await_result(coro):
	if asyncio.iscoroutinefunction(coro):
		coro = coro()
	if __debug__:
		assert asyncio.iscoroutine(coro), coro
	return loop.run_until_complete(coro)
future = asyncio.ensure_future