import asyncio
completes = 0
def complete(coro, loop = None):
	print('started a complete!')
	global completes
	completes += 1
	# assert completes == 1
	if loop == None:
		loop = asyncio.get_event_loop()
	if asyncio.iscoroutinefunction(coro):
		coro = coro()

	assert asyncio.iscoroutine(coro), type(coro)

	return loop.run_until_complete(coro)