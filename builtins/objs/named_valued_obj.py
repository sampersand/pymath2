from typing import Any
from pymath2 import Undefined
from .named_obj import NamedObj
from .valued_obj import ValuedObj
class NamedValuedObj(NamedObj, ValuedObj):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		NamedObj.__init__(self, name)
		ValuedObj.__init__(self, value)

	def __str__(self) -> str:
		return ValuedObj.__str__(self) if self.hasvalue else NamedObj.__str__(self)

	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(type(self).__qualname__,
					self.name,
					self.value)

	def __eq__(self, other):
		if self.name is Undefined:
			return self is other
		if NamedObj.__eq__(self, other) and self.name is not Undefined:
			return True
		return ValuedObj.__eq__(self, other) and self.value is not Undefined

	@property
	def no_value(self):
		return type(self)(name = self.name)

