from typing import Any
from pymath2 import Undefined
from pymath2.objs.named_obj import NamedObj
from pymath2.objs.valued_obj import ValuedObj
class NamedValuedObj(NamedObj, ValuedObj):
	def __init__(self, name: str = Undefined, value: Any = Undefined):
		NamedObj.__init__(self, name)
		ValuedObj.__init__(self, value)

	def __str__(self) -> str:
		return ValuedObj.__str__(self) if self.hasvalue else NamedObj.__str__(self)

	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(type(self).__qualname__,
					self.name,
					self.value)

