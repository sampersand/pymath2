from typing import Any
from pymath2 import Undefined, override
from .named_obj import NamedObj
from .valued_obj import ValuedObj
class NamedValuedObj(NamedObj, ValuedObj):

	@override(NamedObj, ValuedObj)
	def __str__(self) -> str:
		return ValuedObj.__str__(self) if self.hasvalue else NamedObj.__str__(self)

	@override(NamedObj, ValuedObj)
	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(self.__class__.__name__, self.name, self.value)
