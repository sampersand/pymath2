from typing import TYPE_CHECKING
from pymath2 import override, final
from .number import Number
from .derivable import Derivable
from .objs.user_obj import UserObj
if __debug__: #only need these if using assertions
	from .objs.math_obj import MathObj
	from pymath2 import inloop

from pymath2 import Undefined

class Constant(Number):

	@override(Derivable)
	async def _aderiv(self, du: 'Variable') -> 0:
		assert inloop()
		if __debug__:
			from .variable import Variable
		assert isinstance(du, Variable), 'Can only take derivative with regards to Variable, not {}'.format(type(du))
		return 0

	@override(Number)
	async def __arepr__(self) -> str:
		assert inloop()
		if await self._ahasvalue:
			value_str = await self._avalue
			assert not isinstance(value_str, MathObj), 'value cannot be a MathObj.'
				# we will be calling str, so we need this.
			value_str = str(value_str)
		else:
			value_str = ''
		return '{}({})'.format(type(self).__qualname__, value_str)

@final
class UserConstant(UserObj, Constant):

	@override(Constant)
	async def __ainit__(self, value: Constant._valid_types) -> None:
		assert inloop()
		await super().__ainit__(value = value)






