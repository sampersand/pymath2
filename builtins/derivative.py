import asyncio
from typing import Any
from pymath2 import Undefined, override, final, complete, ensure_future
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
class Derivative(NamedValuedObj):
	@override(NamedValuedObj)
	async def __ainit__(self, value: NamedValuedObj, **kwargs) -> None:
		assert 'name' not in kwargs
		an = ensure_future(value._ahasattr('_aname'))
		av = ensure_future(value._ahasattr('_avalue'))
		assert await an
		assert await av

		await super().__ainit__(name = 'd{}'.format(await value._aname), value = value, **kwargs)

	@final
	def __truediv__(self, other: 'Derivative') -> 'UnseededFunction':
		assert False, "don't use non-async functions!"
		if not isinstance(other, Derivative):
			return super().__truediv__(self, other)
		return self._complete_func(other)

	async def __atruediv__(self, other):
		sv = ensure_future(self._avalue)
		ov = ensure_future(other._avalue)
		await sv
		await ov
		await ov.__asetattr__('_old_value_before_deriv', await ov._avalue)
		await ov._avalue_deleter()

		ret = await sv.deriv(ov)
		await ov._avalue_setter(ov._old_value_before_deriv)
		await ov.__adelattr__('_old_value_before_deriv')
		return ret

	@override(NamedValuedObj)
	async def __astr__(self) -> str:
		return self._aname

@final
class UserDerivative(Derivative):
	@override(Derivative)
	async def __ainit__(self, value):
		await super().__ainit__(value = value)







