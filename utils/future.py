from typing import Any, Callable
import asyncio
class Future():
	def __init__(self, inp_func: Callable) -> None:
		self._future_func = inp_func
	# async def __await__(self):
	# 	if not asyncio.iscoroutine(self._future_func):
	# 		return self._future_func()
	# 	return await self._future_func()

	@property
	def hasval(self) -> bool:
		return hasattr(self, '_val')
	@property
	def val(self) -> Any:
		if not self.hasval:
			self._val = self._future_func()
		return self._val

	def __str__(self) -> str:
		# if not self.hasval:
		# 	return super().__str__()
		return str(self.val)