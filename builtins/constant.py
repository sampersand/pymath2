from typing import Any
from pymath2 import Undefined, override, final
from .objs.valued_obj import ValuedObj
from .derivable import Derivable


class Constant(ValuedObj, Derivable):

	@override(Derivable)
	def deriv(self, du: 'Variable') -> 0:
		return 0

	@override(ValuedObj)
	def __repr__(self) -> str:
		return '{}({})'.format(self.__class__.__name__,
							   repr(self.value) if self.hasvalue else '')

@final
class UserConstant(Constant):
	@override(Constant)
	def __init__(self, value):
		super().__init__(value = value)