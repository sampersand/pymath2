import asyncio
def complete(coro, loop = None):
	if loop == None:
		loop = asyncio.get_loop()
	if asyncio.iscoroutinefunction(coro):
		coro = coro()
	if __debug__:
		assert asyncio.iscoroutine(coro), type(coro)
	return loop.run_until_complete(coro)