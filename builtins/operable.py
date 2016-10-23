from inspect import stack

from typing import Any
from pymath2 import Undefined, complete, final, future
from .objs.math_obj import MathObj

class Operable(MathObj):
	async def __ainit__(self, *args, **kwargs):
		ainit = future(super().__ainit__(*args, **kwargs))
		await ainit
	async def _get_oper(self, other: Any = Undefined) -> 'SeededOperator':
		from pymath2.builtins.functions.operator import opers
		if other is Undefined:
			return await opers[stack()[1][3]].__acall__(self)
		return await opers[stack()[1][3]].__acall__(self, other)

	@final
	def __add__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __aadd__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __sub__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __asub__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __mul__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __amul__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __truediv__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __atruediv__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __floordiv__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __afloordiv__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __mod__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __amod__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __pow__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __apow__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __radd__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __aradd__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rsub__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __arsub__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rmul__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __armul__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rtruediv__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __artruediv__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rfloordiv__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __arfloordiv__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rmod__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __armod__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __rpow__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __arpow__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __lt__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __alt__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __gt__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __agt__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __le__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __ale__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __gt__(self, other: Any) -> 'SeededOperator': return self._complete_func(other)
	async def __agt__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __abs__(self) -> 'SeededOperator': self._complete_func()
	async def __aabs__(self) -> 'SeededOperator': return await self._get_oper()
	
	@final
	def __neg__(self) -> 'SeededOperator': self._complete_func()
	async def __aneg__(self) -> 'SeededOperator': return await self._get_oper()

	@final
	def __pos__(self) -> 'SeededOperator': self._complete_func()
	async def __apos__(self) -> 'SeededOperator': return await self._get_oper()

	@final
	def __invert__(self) -> 'SeededOperator': self._complete_func()
	async def __ainvert__(self) -> 'SeededOperator': return await self._get_oper()


	@final
	def __and__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __aand__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)

	@final
	def __or__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __aor__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __xor__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __axor__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __lshift__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __alshift__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __rshift__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __arshift__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)


	@final
	def __rand__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __arand__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __ror__(self, other: Any) -> 'SeededOperator': return self._complete_func()
	async def __aror__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __rxor__(self, other: Any) -> 'SeededOperator': return complete(self.__arxor__(other))
	async def __arxor__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __rlshift__(self, other: Any) -> 'SeededOperator': return complete(self.__arlshift__(other))
	async def __arlshift__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
	
	@final
	def __rrshift__(self, other: Any) -> 'SeededOperator': return complete(self.__arrshift__(other))
	async def __arrshift__(self, other: Any) -> 'SeededOperator': return await self._get_oper(other)
