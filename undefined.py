from pymath2.exceptions.not_defined_error import NotDefinedError
class UndefinedClass():
	def __str__(self):
		return 'Undefined'
	def __add__(self, other): return self
	def __sub__(self, other): return self
	def __mul__(self, other): return self
	def __truediv__(self, other): return self
	def __floordiv__(self, other): return self
	def __mod__(self, other): return self
	def __pow__(self, other): return self

	def __radd__(self, other): return self
	def __rsub__(self, other): return self
	def __rmul__(self, other): return self
	def __rtruediv__(self, other): return self
	def __rfloordiv__(self, other): return self
	def __rmod__(self, other): return self
	def __rpow__(self, other): return self

	def __eq__(self, other): return other is self
	def __ne__(self, other): return other is not self
	def __lt__(self, other): return self
	def __gt__(self, other): return self
	def __le__(self, other): return self
	def __gt__(self, other): return self

	def __abs__(self): return self
	def __neg__(self): return self
	def __pos__(self): return self
	def __invert__(self): return self

	def __and__(self, other): return self
	def __or__(self, other): return self
	def __xor__(self, other): return self
	def __lshift__(self, other): return self
	def __rshift__(self, other): return self

	def __rand__(self, other): return self
	def __ror__(self, other): return self
	def __rxor__(self, other): return self
	def __rlshift__(self, other): return self
	def __rrshift__(self, other): return self

	def __bool__(self): raise NotDefinedError('__bool__')
	def __float__(self): raise NotDefinedError('__float__')
	def __int__(self): raise NotDefinedError('__int__')
	def __complex__(self): raise NotDefinedError('__complex__')

	@property
	def hasvalue(self):
		return False
Undefined = UndefinedClass()













