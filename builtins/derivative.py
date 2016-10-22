import asyncio
from typing import Any
from pymath2 import Undefined, override, final, complete
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
class Derivative(NamedValuedObj):
	@override(NamedValuedObj)
	async def __ainit__(self, value: NamedValuedObj, **kwargs) -> None:
		assert 'name' not in kwargs
		assert hasattr(value, 'name')
		assert hasattr(value, 'value'), value

		await super().__ainit__(name = 'd{}'.format(value.name), value = value, **kwargs)

	@final
	def __truediv__(self, other: 'Derivative') -> 'UnseededFunction':
		assert False, "don't use non-async functions!"
		if not isinstance(other, Derivative):
			return super().__truediv__(self, other)
		return complete(self.__atruediv__(other))

	async def __atruediv__(self, other):
		other.value._old_value_before_deriv = other.value.value
		del other.value.value
		ret = await self.value.deriv(other.value)
		other.value.value = other.value._old_value_before_deriv
		del other.value._old_value_before_deriv
		return ret

	@override(NamedValuedObj)
	async def __astr__(self) -> str:
		return self._aname

@final
class UserDerivative(Derivative):
	@override(Derivative)
	async def __ainit__(self, value):
		await super().__ainit__(value = value)







