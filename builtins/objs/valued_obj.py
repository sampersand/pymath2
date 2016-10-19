from typing import Any
from pymath2 import Undefined
from .math_obj import MathObj
class ValuedObj(MathObj):
	def __init__(self, value: Any = Undefined) -> None:
		MathObj.__init__(self)
		self._value = value

	def value() -> dict:
		def fget(self) -> (Any, Undefined):
			return self._value
		def fset(self, val: Any) -> None:
			self._value = val
		def fdel(self) -> None:
			self._value = Undefined
		return locals()
	value = property(**value())

	def isconst(self, du):
		return self != du

	@property
	def hasvalue(self) -> bool:
		return (self.value) is not Undefined #await

	def __str__(self) -> str:
		return self.generic_str('unvalued') if not self.hasvalue else str(self.value)

	def __repr__(self) -> str:
		return '{}({!r})'.format(type(self).__qualname__, self.value)

	def __abs__(self) -> float:
		return abs(float(self))
	def __bool__(self) -> bool:
		return bool(self.value)
	def __int__(self) -> int:
		return int(self.value)
	def __float__(self) -> float:
		return float(self.value)
	def __complex__(self) -> complex:
		return complex(self.value)


	def __eq__(self, other: Any) -> bool:
		if not hasattr(other, 'value'):
			return False
		return self.value == other.value

	def deriv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		return Undefined

	@property
	def no_value(self):
		return type(self)()


	def d(self, other):
		from pymath2.builtins.derivative import Derivative
		return Derivative(self) / Derivative(other)