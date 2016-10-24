import asyncio
def complete(coro, loop = None):
	if loop == None:
		try:
			loop = asyncio.get_event_loop()
		except RuntimeError:
			loop = asyncio.new_event_loop()
	if asyncio.iscoroutinefunction(coro):
		coro = coro()

	assert asyncio.iscoroutine(coro), type(coro)
	return loop.run_until_complete(coro)