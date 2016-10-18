from typing import Any
from pymath2 import Undefined, await_result
from .named_obj import NamedObj
from .valued_obj import ValuedObj
class NamedValuedObj(NamedObj, ValuedObj):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		NamedObj.__init__(self, name)
		ValuedObj.__init__(self, value)

	def __str__(self) -> str:
		return ValuedObj.__str__(self) if await_result(self.hasvalue) else NamedObj.__str__(self)

	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(type(self).__qualname__,
					self.name,
					await_result(self.value))

	def __eq__(self, other):
		return NamedObj.__eq__(self, other) or ValuedObj.__eq__(self, other)


