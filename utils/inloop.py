from asyncio import get_event_loop
def inloop():
	return get_event_loop().is_running()

