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
	def hasvalue(self) -> bool:
		return hasattr(self, '_value')
	@property
	def value(self) -> Any:
		if not self.hasvalue:
			self._value = self._future_func()
		return self._value

	def __str__(self) -> str:
		# if not self.hasvalue:
		# 	return super().__str__()
		return str(self.value)