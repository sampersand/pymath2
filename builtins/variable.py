from typing import Any
from pymath2 import Undefined, override, final
from .objs.named_valued_obj import NamedValuedObj
from .derivable import Derivable
class Variable(NamedValuedObj, Derivable):

	@override(Derivable)
	async def _aisconst(self, du: 'Variable') -> bool:
		return self is not du and self.name != du.name

	@override(Derivable)
	def deriv(self, du: 'Variable') -> (0, 1):
		return self.scrub(int(not self.isconst(du)))

	@override(NamedValuedObj)
	def __repr__(self) -> str:
		return '{}({})'.format(self.__class__.__name__, 
			', '.join(x for x in (repr(self.name), 'value=' + repr(self.value) if self.hasvalue else Undefined) if x is not Undefined))


@final
class UserVariable(Variable):
	@override(Variable)
	def __init__(self, name = Undefined, value = Undefined):
		super().__init__(value = value, name = name)
