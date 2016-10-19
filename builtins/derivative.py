import asyncio
from typing import Any
from pymath2 import Undefined, Override
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
class Derivative(NamedValuedObj):
	@Override(NamedValuedObj)
	def __init__(self, value: NamedValuedObj, **kwargs) -> None:
		if __debug__:
			assert 'name' not in kwargs
			assert hasattr('name', value)
			assert hasattr('value', value)
		super().__init__(name = 'd{}'.format(value.name), value = value, **kwargs)

	def __truediv__(self, other: 'Derivative') -> 'UnseededFunction':
		if not isinstance(other, Derivative):
			return NotImplemented
		return self.value.deriv(other.value)

	@Override(NamedValuedObj)
	def __str__(self) -> str:
		return self.name








