from typing import Any
from pymath2 import Undefined, Override
from .objs.valued_obj import ValuedObj
from .derivable import Derivable


class Constant(ValuedObj, Derivable):

	@Override(Derivable)
	def deriv(self, du: 'Variable') -> 0:
		return 0

	@Override(ValuedObj)
	def __repr__(self) -> str:
		return '{}({})'.format(self.__class__.__name__,
							   repr(self.value) if self.hasvalue else '')
