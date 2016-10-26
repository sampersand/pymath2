from . import get_event_loop
def inloop():
	event_loop = get_event_loop()
	assert event_loop != None #maybe another assert other than none?
	return event_loop.is_running()

