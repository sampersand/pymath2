from typing import Any
from pymath2 import Undefined
from pymath2.objs import MathObj
class ValuedObj(MathObj):
	def __init__(self, value: Any = Undefined) -> None:
		MathObj.__init__(self)
		
		self._value = value

	def value():
		def fget(self) -> (Any, Undefined):
			return self._value
		def fset(self, val: Any) -> None:
			self._value = val
		return locals()
	value = property(**value())

	@property
	def hasvalue(self) -> bool:
		return self.value is not Undefined

	def __str__(self) -> str:
		return self.generic_str('unvalued') if not self.hasvalue else str(self.value)

	def __repr__(self) -> str:
		return '{}({!r})'.format(type(self).__qualname__, self.value)