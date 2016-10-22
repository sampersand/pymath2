from typing import Any
from pymath2 import Undefined, override, final, complete, future
from .math_obj import MathObj
from pymath2.builtins.operable import Operable
from pymath2.builtins.derivable import Derivable
class ValuedObj(Operable, Derivable):

	@override(Operable, Derivable)
	async def __ainit__(self, value: Any = Undefined, **kwargs) -> None:
		supi = future(super().__ainit__(**kwargs))
		val  = future(self._avalue_setter(value))
		await supi
		await val

	@final
	def value():
		@final
		def fget(self) -> (Any, Undefined):
			return complete(self._avalue)
		@final
		def fset(self, val: Any) -> None:
			return complete(self._avalue_setter(val))
		@final
		def fdel(self) -> None:
			return complete(self._avalue_deleter())
		return locals()
	value = property(**value())

	@property
	async def _avalue(self):
		return self._value

	async def _avalue_setter(self, val: Any) -> None:
		self._value = val

	async def _avalue_deleter(self) -> None:
		self._value = Undefined

	@property
	@final
	def hasvalue(self) -> bool:
		return complete(self._ahasvalue)

	@property
	async def _ahasvalue(self) -> bool:
		return await self._avalue is not Undefined #await

	@override(Derivable)
	async def _aisconst(self, du: 'Variable'):
		return self != du

	@final
	def __abs__(self) -> float:
		return complete(self.__aabs__())
	async def __aabs__(self) -> float:
		return abs(self.__afloat__(self))

	@final
	def __bool__(self) -> bool: 
		assert 0, 'make sure this isnt being used incorrectly!'
		return complete(self.__aabs__())
	async def __abool__(self) -> bool:
		return bool(await self._avalue)

	@final
	def __int__(self) -> int:
		return complete(self.__aint__())
	async def __aint__(self) -> int:
		return int(self.value)

	@final
	def __float__(self) -> float:
		return complete(self.__afloat__())
	async def __afloat__(self) -> float:
		return float(self.value) 

	@final
	def __complex__(self) -> complex:
		return complete(self.__acomplex__())
	async def __acomplex__(self) -> complex:
		return complex(self.value)

	@final
	def __round__(self, digits: int) -> (int, float):
		return complete(self.__around__())

	async def __around__(self, digits: int) -> (int, float):
		return round(float(self), int(digits))

	@override(MathObj)
	async def __aeq__(self, other: Any) -> bool:
		other = self.scrub(other)
		if not hasattr(other, 'value'):
			return False
		myv = future(self._avalue)
		otv = future(other._avalue)
		myv = await myv
		otv = await otv
		if myv == otv and myv is not Undefined:
			return True
		return super().__eq__(other)

	@override(Operable, Derivable)
	async def __astr__(self) -> str:
		value = future(self._avalue)
		hasvalue = future(self._ahasvalue)
		return self.generic_str('unvalued') if not await hasvalue else\
			(await self.async_getattr(await value, '__str__'))()

	@override(Operable, Derivable)
	async def __arepr__(self) -> str:
		return '{}({})'.format(self.__class__.__name__,\
				(await self.async_getattr(await self._avalue))())









