from typing import Any
from pymath2 import Undefined, override, final, complete, FinishSet
from .math_obj import MathObj
from pymath2.builtins.operable import Operable
from pymath2.builtins.derivable import Derivable
if __debug__:
	from pymath2 import inloop
class ValuedObj(Operable, Derivable):
	_valid_types = {type(Undefined)}
	@override(Operable, Derivable)
	async def __ainit__(self, value: Any = Undefined, **kwargs) -> None:
		assert inloop()
		if type(value) not in self._valid_types:
			raise TypeError('Cannot have type {} as a value for {}. Valid Types: {}'.format(
																		   type(value).__qualname__,
																		   type(self).__qualname__,
																		   self._valid_types, ))

		async with FinishSet() as f:
			f.future(super().__ainit__(**kwargs))
			f.future(self._avalue_setter(value))

	@final
	def value():
		@final
		def fget(self) -> (Any, Undefined):
			assert not inloop()
			return complete(self._avalue)
		@final
		def fset(self, val: Any) -> None:
			assert not inloop()
			return complete(self._avalue_setter(val))
		@final
		def fdel(self) -> None:
			assert not inloop()
			return complete(self._avalue_deleter())
		return locals()
	value = property(**value())

	@property
	async def _avalue(self):
		assert inloop()
		return self._value

	async def _avalue_setter(self, val: Any) -> None:
		assert inloop()
		await self.__asetattr__('_value', val)

	async def _avalue_deleter(self) -> None:
		assert inloop()
		await self._avalue_setter(Undefined)

	@property
	@final
	def hasvalue(self) -> bool:
		assert not inloop()
		return complete(self._ahasvalue)

	@property
	async def _ahasvalue(self) -> bool:
		assert inloop()
		return await self._avalue is not Undefined #await

	@override(Derivable)
	async def _aisconst(self, du: 'Variable'):
		assert inloop()
		return self != du

	@final
	def __abs__(self) -> float:
		assert not inloop()
		return complete(self.__aabs__())
	async def __aabs__(self) -> float:
		return abs(self.__afloat__(self))

	@final
	def __bool__(self) -> bool: 
		assert not inloop()
		return complete(self.__aabs__())
	async def __abool__(self) -> bool:
		assert inloop()
		return bool(await self._avalue)

	@final
	def __int__(self) -> int:
		assert not inloop()
		return complete(self.__aint__())
	async def __aint__(self) -> int:
		assert inloop()
		return int(await self._avalue)

	@final
	def __float__(self) -> float:
		assert not inloop()
		return complete(self.__afloat__())
	async def __afloat__(self) -> float:
		assert inloop()
		return float(await self._avalue) 

	@final
	def __complex__(self) -> complex:
		assert not inloop()
		return complete(self.__acomplex__())
	async def __acomplex__(self) -> complex:
		assert inloop()
		return complex(self._avalue)

	@final
	def __round__(self, digits: int) -> (int, float):
		assert not inloop()
		return complete(self.__around__())

	async def __around__(self, digits: int) -> (int, float):
		assert inloop()
		return round(await self.__afloat__(), int(digits))

	@override(MathObj)
	async def __aeq__(self, other: Any) -> bool:
		assert inloop()
		other = self.scrub(other)
		if not hasattr(other, 'value'):
			return False
		async with FinishSet() as f:
			myv = f.future(self._avalue)
			otv = f.future(other._avalue)
		if myv.result() == otv.result() and myv.result() is not Undefined:
			return True
		return super().__eq__(other)

	@override(Operable, Derivable)
	async def __astr__(self) -> str:
		assert inloop()
		async with FinishSet() as f: 
			value = f.future(self._avalue)
			hasvalue = f.future(self._ahasvalue)
		if not hasvalue.result():
			return self.generic_str('unvalued')
		str_attr = await self.get_asyncattr(value.result(), '__str__')
		assert not isinstance(str_attr, MathObj)
		return str(str_attr)

	@override(Operable, Derivable)
	async def __arepr__(self) -> str:
		assert inloop()
		value = await self._avalue
		value_attr = await self.get_asyncattr(self._avalue)
		assert not isinstance(value_attr, MathObj)
		value_repr = repr(value_attr)
		return '{}({})'.format(self.__class__.__name__, value_repr)









