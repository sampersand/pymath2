import asyncio
from typing import Any
from pymath2 import Undefined, override, final
# from .functions.unseeded_function import 'UnseededFunction'
from .objs.named_valued_obj import NamedValuedObj
class Derivative(NamedValuedObj):
	@override(NamedValuedObj)
	def __init__(self, value: NamedValuedObj, **kwargs) -> None:
		if __debug__:
			v = str(value) 
			assert 'name' not in kwargs
			assert hasattr(value, 'name')
			assert hasattr(value, 'value'), value
		super().__init__(name = 'd{}'.format(value.name), value = value, **kwargs)

	def __truediv__(self, other: 'Derivative') -> 'UnseededFunction':
		if not isinstance(other, Derivative):
			return NotImplemented
		other.value._old_value_before_deriv = other.value.value
		del other.value.value
		ret = self.value.deriv(other.value)
		other.value.value = other.value._old_value_before_deriv
		del other.value._old_value_before_deriv
		return ret

	@override(NamedValuedObj)
	def __str__(self) -> str:
		return self.name

@final
class UserDerivative(Derivative):
	@override(Derivative)
	def __init__(self, value):
		super().__init__(value = value)







