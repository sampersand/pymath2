import asyncio
from typing import Any
from pymath2 import Undefined, override, final, complete, finish
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
if __debug__:
	from .objs.valued_obj import ValuedObj
	from .objs.named_obj import NamedObj
	from pymath2 import inloop
class Derivative(NamedValuedObj):
	@override(NamedValuedObj)
	async def __ainit__(self, value: NamedValuedObj, **kwargs) -> None:
		assert inloop()

		assert 'name' not in kwargs # it'll be generated.
		assert isinstance(value, ValuedObj) # or at least has ._aname
		assert isinstance(value, NamedObj) #or at least has ._avalue

		await super().__ainit__(name = 'd{}'.format(await value._aname), value = value, **kwargs)

	@final
	def __truediv__(self, other: 'Derivative') -> 'UnseededFunction':
		assert not inloop()
		if not isinstance(other, Derivative):
			return super().__truediv__(self, other)
		return complete(self.__atruediv__(other))

	async def __atruediv__(self, other):
		assert inloop()
		async with finish():
			ov = future(self._avalue)
			sv = future(other._avalue)
		ov = ov.result()
		if __debug__:
			import Variable
			assert isinstance(ov, Variable), 'cannot take deriv with regards to a non-variable'
		await ov.__asetattr__('_old_value_before_deriv', await ov._avalue())
		await ov._avalue_deleter()

		ret = await sv.result().deriv(ov)

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
		assert inloop()
		await super().__ainit__(value = value)







