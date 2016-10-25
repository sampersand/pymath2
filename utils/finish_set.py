from . import ensure_future, iscoroutine
from .inloop import inloop
from asyncio import Lock
class FinishSet(Lock, set):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		assert not self.locked(), "super shouldn't lock me!"
		self._locked = True # this is really bad, but needs to be here because we cant await acqiure
		assert self.locked()
		# await self.acquire() # will be locked before and after entered

	def add(self, fut):
		# maybe assert loop?
		assert not self.locked(), "Shouldn't add in values before entered!"
		assert isinstance(fut, FutureClass)
		super().add(fut)

	async def _join(self):
		assert inloop()
		assert self.locked(), "Should re-lock before joining!"
		while self:
			await self.pop()

	async def __aenter__(self):
		assert not self # shouldn't have values added in beforehand - self.add should have caught this
		assert self.locked(), "Shouldn't be unlocked before entered!"
		self.release()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		assert not self.locked()
		await self.acquire()
		assert self.locked() # this is redudant with the line before it
		await self._join()
		if exc_val:
			raise exc_val

	def future(self, coro):
		fut = FutureClass(coro, self)
		self.add(fut)
		return fut

class FutureClass():
	def __init__(self, coro, finish_set):
		assert iscoroutine(coro)
		assert isinstance(finish_set, FinishSet)
		self.coro = ensure_future(coro)
		self.finish_set = finish_set
	def __await__(self):
		assert inloop()
		res = self.coro.__await__()
		if self not in self.finish_set:
			assert self.finish_set.locked() # if it's here, it's in the process of '_join'ing
			return res
		assert not self.finish_set.locked(), "Shouldn't be awaiting outside of a loop" # see below
			# if we are being awaited outside the with loop, we should have been completed already
			# note to self: if need to use this out of the loop, use 'result'
		self.finish_set.remove(self) # so you can 'pop' in join and not crash
		return res

	def result(self):
		return self.coro.result()

	def done(self):
		return self.coro.done()

