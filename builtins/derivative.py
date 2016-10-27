import asyncio
from typing import Any
from pymath2 import Undefined, override, final, complete, finish
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
from .objs.valued_obj import ValuedObj #debug
from .objs.named_obj import NamedObj #debug
from .objs.user_obj import UserObj
from pymath2 import inloop #debug
from .variable import Variable
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
		async with finish() as f:
			sv = f.future(self._avalue)
			ov = f.future(other._avalue)
		return await Derivative._a_get_deriv(sv.result(), ov.result())
	@staticmethod
	async def _a_get_deriv(sv, ov):
		assert inloop()
		# if not isinstance
		if not isinstance(ov, Variable):
			raise TypeError('Can only take deriv with regards to a Variable, not {}'.format(type(ov)))
		await ov.__asetattr__('_old_value_before_deriv', await ov._avalue)
		await ov._avalue_deleter()

		ret = await sv._aderiv(ov)

		await ov._avalue_setter(ov._old_value_before_deriv)
		await ov.__adelattr__('_old_value_before_deriv')
		return ret

	@override(NamedValuedObj)
	async def __astr__(self) -> str:
		assert inloop()
		return self._aname

@final
class UserDerivative(UserObj, Derivative):
	@override(UserObj, Derivative)
	async def __ainit__(self, value):
		assert inloop()
		await super().__ainit__(value = value)







