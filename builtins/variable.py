from typing import Any
from pymath2 import Undefined
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.objs.operable import Operable
class Variable(NamedValuedObj, Operable):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		super().__init__(name = name, value = value)

	def isconst(self, du):
		return self is not du and self.name != du.name
		# return self != du

	def deriv(self, du: 'Variable') -> (0, 1):
		return int(not self.isconst(du))

		# return self if self == du else int(not self.isconst(du))
	def __repr__(self) -> str:
		return '{}({})'.format(type(self).__qualname__, ', '.join(repr(x) for x in 
			(self.name, self.value) if x is not Undefined))
