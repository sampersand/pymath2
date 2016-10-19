import asyncio
# loop = asyncio.get_event_loop()
def await_result(coro, event_loop = None):
	if event_loop == None:
		event_loop = asyncio.get_event_loop()
	if asyncio.iscoroutinefunction(coro):
		coro = coro()
	if __debug__:
		# assert hasattr(coro, '__await__'), coro 
		assert asyncio.iscoroutine(coro), type(coro)
	return event_loop.run_until_complete(coro)
future = asyncio.ensure_future