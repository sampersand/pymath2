from typing import Any
from pymath2 import Undefined
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.objs.operable import Operable
class Variable(NamedValuedObj, Operable):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		super().__init__(name = name, value = value)

	async def deriv(self, du: 'Variable') -> (0, 1, 'self'):
		return int(not await self.isconst(du))
		# return self if self == du else int(not self.isconst(du))
	def __repr__(self) -> str:
		return '{}({})'.format(type(self).__qualname__, ', '.join(repr(x) for x in 
			(self.name, await_result(self.value)) if x is not Undefined))
