from typing import Any
from pymath2 import Undefined, override
from .math_obj import MathObj
from pymath2.builtins.operable import Operable
from pymath2.builtins.derivable import Derivable
class ValuedObj(Operable, Derivable):

	@override(Operable, Derivable)
	def __init__(self, value: Any = Undefined, **kwargs) -> None:
		super().__init__(**kwargs)
		self._value = value

	@property
	def value(self) -> (Any, Undefined):
		return self._value

	@value.setter
	def value(self, val: Any) -> None:
		self._value = val

	@value.deleter
	def value(self) -> None:
		self._value = Undefined

	@property
	def hasvalue(self) -> bool:
		return self.value is not Undefined #await

	@override(Derivable)
	def isconst(self, du: 'Variable'):
		return self != du

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

	def __round__(self, digits: int) -> (int, float):
		return round(float(self), int(digits))

	def __eq__(self, other: Any) -> bool:
		other = self.scrub(other)
		if not hasattr(other, 'value'):
			return False
		if self.value == other.value and self.value is not Undefined:
			return True
		return super().__eq__(other)

	@override(Operable, Derivable)
	def __str__(self) -> str:
		return self.generic_str('unvalued') if not self.hasvalue else str(self.value)

	@override(Operable, Derivable)
	def __repr__(self) -> str:
		return '{}({!r})'.format(self.__class__.__name__, self.value)


