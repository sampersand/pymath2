import inspect
from .math_obj import MathObj
class Operable(MathObj):
	def _get_oper(self, other):
		from pymath2.functions.operator import opers
		return opers[inspect.stack()[1][3]](self, other)
	def __add__(self, other): return self._get_oper(other)
	def __sub__(self, other): return self._get_oper(other)
	def __mul__(self, other): return self._get_oper(other)
	def __truediv__(self, other): return self._get_oper(other)
	def __floordiv__(self, other): return self._get_oper(other)
	def __mod__(self, other): return self._get_oper(other)
	def __pow__(self, other): return self._get_oper(other)

	def __radd__(self, other): return self._get_oper(other)
	def __rsub__(self, other): return self._get_oper(other)
	def __rmul__(self, other): return self._get_oper(other)
	def __rtruediv__(self, other): return self._get_oper(other)
	def __rfloordiv__(self, other): return self._get_oper(other)
	def __rmod__(self, other): return self._get_oper(other)
	def __rpow__(self, other): return self._get_oper(other)

	# def __eq__(self, other): return other is self
	# def __ne__(self, other): return not (self == other)
	def __lt__(self, other): return self._get_oper(other)
	def __gt__(self, other): return self._get_oper(other)
	def __le__(self, other): return self._get_oper(other)
	def __gt__(self, other): return self._get_oper(other)

	def __abs__(self): return self._get_oper(other)
	def __neg__(self): return self._get_oper(other)
	def __pos__(self): return self._get_oper(other)
	def __invert__(self): return self._get_oper(other)

	def __and__(self, other): return self._get_oper(other)
	def __or__(self, other): return self._get_oper(other)
	def __xor__(self, other): return self._get_oper(other)
	def __lshift__(self, other): return self._get_oper(other)
	def __rshift__(self, other): return self._get_oper(other)

	def __rand__(self, other): return self._get_oper(other)
	def __ror__(self, other): return self._get_oper(other)
	def __rxor__(self, other): return self._get_oper(other)
	def __rlshift__(self, other): return self._get_oper(other)
	def __rrshift__(self, other): return self._get_oper(other)

	def __bool__(self): raise NotDefinedError('__bool__')
	def __float__(self): raise NotDefinedError('__float__')
	def __int__(self): raise NotDefinedError('__int__')
	def __complex__(self): raise NotDefinedError('__complex__')

