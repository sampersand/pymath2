from typing import Any
from pymath2 import final
# @final
class UndefinedClass():
	def __str__(self) -> str: return 'Undefined'
	def __repr__(self) -> str: return '{}()'.format(self.__class__.__name__)

	def __add__(self, other: Any) -> 'self': return self
	def __sub__(self, other: Any) -> 'self': return self
	def __mul__(self, other: Any) -> 'self': return self
	def __truediv__(self, other: Any) -> 'self': return self
	def __floordiv__(self, other: Any) -> 'self': return self
	def __mod__(self, other: Any) -> 'self': return self
	def __pow__(self, other: Any) -> 'self': return self

	def __radd__(self, other: Any) -> 'self': return self
	def __rsub__(self, other: Any) -> 'self': return self
	def __rmul__(self, other: Any) -> 'self': return self
	def __rtruediv__(self, other: Any) -> 'self': return self
	def __rfloordiv__(self, other: Any) -> 'self': return self
	def __rmod__(self, other: Any) -> 'self': return self
	def __rpow__(self, other: Any) -> 'self': return self

	def __eq__(self, other: Any) -> bool: return other is self
	def __ne__(self, other: Any) -> bool: return not (self == other)
	def __lt__(self, other: Any) -> 'self': return self
	def __gt__(self, other: Any) -> 'self': return self
	def __le__(self, other: Any) -> 'self': return self
	def __gt__(self, other: Any) -> 'self': return self

	def __abs__(self) -> 'self': return self
	def __neg__(self) -> 'self': return self
	def __pos__(self) -> 'self': return self
	def __invert__(self) -> 'self': return self

	def __and__(self, other: Any) -> 'self': return self
	def __or__(self, other: Any) -> 'self': return self
	def __xor__(self, other: Any) -> 'self': return self
	def __lshift__(self, other: Any) -> 'self': return self
	def __rshift__(self, other: Any) -> 'self': return self

	def __rand__(self, other: Any) -> 'self': return self
	def __ror__(self, other: Any) -> 'self': return self
	def __rxor__(self, other: Any) -> 'self': return self
	def __rlshift__(self, other: Any) -> 'self': return self
	def __rrshift__(self, other: Any) -> 'self': return self

	def __bool__(self) -> bool: return False
	# def __float__(self): raise AttributeError("Cannot take the f__float__")
	# def __int__(self): raise AttributeError("Cannot take the f__int__")
	# def __complex__(self): raise AttributeError("Cannot take the f__complex__")

	async def __await__(self) -> 'self': return self

	@property
	def hasvalue(self) -> bool:
		assert 0
		return complete(self._ahasvalue)

	@property
	async def _ahasvalue(self):
		return False

	async def deriv(self, du) -> 'self':
		return self
Undefined = UndefinedClass()













