from typing import Any
from pymath2 import Undefined, await_result
from .math_obj import MathObj
class ValuedObj(MathObj):
	def __init__(self, value: Any = Undefined) -> None:
		MathObj.__init__(self)
		self._value = value

	def value() -> dict:
		async def fget(self) -> (Any, Undefined):
			return self._value
		def fset(self, val: Any) -> None:
			self._value = val
		async def fdel(self) -> None:
			self._value = Undefined
		return locals()
	value = property(**value())

	async def isconst(self, du):
		return self != du

	@property
	async def hasvalue(self) -> bool:
		return (await self.value) is not Undefined

	def __str__(self) -> str:
		return self.generic_str('unvalued') if not await_result(self.hasvalue) else str(await_result(self.value))

	def __repr__(self) -> str:
		return '{}({!r})'.format(type(self).__qualname__, await_result(self.value))

	def __abs__(self) -> float:
		return abs(float(self))
	def __bool__(self) -> bool:
		return bool(await_result(self.value))
	def __int__(self) -> int:
		return int(await_result(self.value))
	def __float__(self) -> float:
		return float(await_result(self.value))
	def __complex__(self) -> complex:
		return complex(await_result(self.value))


	def __eq__(self, other: Any) -> bool:
		if not hasattr(other, 'value'):
			return False
		return await_result(self.value) == await_result(other.value)

	async def deriv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		return Undefined