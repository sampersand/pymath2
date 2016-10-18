import asyncio
def await_result(coro):
	if asyncio.iscoroutinefunction(coro):
		coro = coro()
	if __debug__:
		assert asyncio.iscoroutine(coro)
	return asyncio.get_event_loop().run_until_complete(coro)