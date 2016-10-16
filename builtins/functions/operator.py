from typing import Callable

from pymath2 import Undefined
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
from pymath2.builtins.objs.named_obj import NamedObj
class Operator(UnseededFunction, NamedObj):
	seeded_type = SeededOperator
	is_inverted = False
	def __init__(self, name: str, priority: int, wrapped_function: Callable) -> None:
		UnseededFunction.__init__(self, wrapped_function)
		NamedObj.__init__(self, name)
		self.priority = priority
	@property
	def func_name(self) -> str:
		if __debug__:
			assert len([name for name, oper in opers if self is oper]) == 1
		return next(name for name, oper in opers if self is oper)

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return '{}({!r}, {!r}, {!r})'.format(type(self).__qualname__, self.name, self.priority, self.wrapped_function)

	def is_lower_precedence(self, other: UnseededFunction) -> bool:
		if not hasattr(other, 'priority'):
			raise AttributeError("'{}' needs to have the attriubute 'priority'".format(type(other)))
		return self.priority < other.priority

	def deriv(self, du, *args):
		return Undefined

	# def simplify(self, *args):
	# 	return None

class AddSubOperator(Operator):
	def __init__(self, name: str) -> None:
		if __debug__:
			assert name in {'+', '-'}

		if name == '+':
			wrapped_function = lambda l, r: l.value + r.value
		else:
			wrapped_function = lambda l, r: l.value - r.value

		super().__init__(name, 3, wrapped_function)

	def deriv(self, du, l, r):
		if self.name == '+':
			return l.deriv(du) + r.deriv(du)
		return l.deriv(du) - r.deriv(du)

class MulOperator(Operator):
	def __init__(self):
		super().__init__('*', 2, lambda l, r: l.value * r.value)

	def deriv(self, du, l, r):
		return l.deriv(du) * r + l * r.deriv(du)

class TrueDivOperator(Operator):
	def __init__(self):
		super().__init__('/', 2, lambda l, r: l.value / r.value)

	def deriv(self, du, n, d):
		return (d * n.deriv(du) - n * d.deriv(du)) / d ** 2

class PowOperator(Operator):
	def __init__(self):
		super().__init__('**', 0, lambda b, p: b.value ** p.value)

	def deriv(self, du, b, p):
		bconst = b.isconst(du)
		pconst = p.isconst(du)
		if not bconst and not pconst:
			return 0
		elif not bconst and pconst:
			return p * b ** (p - 1) * b.deriv(du)
		elif bconst and not pconst:
			from pymath2.extensions.functions import ln
			return b ** p * ln(b) * p.deriv(du)
		else:
			if __debug__:
				assert bconst and pconst #only option left
			from pymath2.extensions.functions import ln
			return b ** p * (b.deriv(du) * p / b + p.deriv(du) * ln(b))


class InvertedOperator(Operator):
	is_inverted = True
	def __init__(self, normal_operator: Operator) -> None:
		self.normal_operator = normal_operator
		super().__init__(normal_operator.name, normal_operator.priority, normal_operator.wrapped_function)

	@property
	def wrapped_function(self) -> Callable:
		return self.normal_operator.wrapped_function

	@wrapped_function.setter
	def wrapped_function(self, value) -> None:
		pass

	def deriv(self, du, *args):
		return self.normal_operator.deriv(du, *args[::-1]) #haha! that's how you invert it

opers = {
	'__add__': AddSubOperator('+'),
	'__sub__': AddSubOperator('-'),
	'__mul__': MulOperator(),
	'__truediv__': TrueDivOperator(),
	'__floordiv__': Operator('//', 2, lambda l, r: l.value // r.value),
	'__mod__': Operator('%', 2, lambda l, r: l.value % r.value),
	'__matmul__': Operator('@', 2, lambda l, r: l.value @ r.value),
	'__pow__': PowOperator(),

	'__and__': Operator('&', 5, lambda l, r: l.value & r.value),
	'__or__': Operator('|', 7, lambda l, r: l.value | r.value),
	'__xor__': Operator('^', 6, lambda l, r: l.value ^ r.value),
	'__lshift__': Operator('<<', 4, lambda l, r: l.value << r.value),
	'__rshift__': Operator('>>', 4, lambda l, r: l.value >> r.value),

	# '__eq__': Operator('==', lambda a, b: a == b),
	# '__ne__': Operator('', lambda l, r: l.value  r.value),
	'__lt__': Operator('<', 8, lambda l, r: l.value < r.value),
	'__gt__': Operator('>', 8, lambda l, r: l.value > r.value),
	'__le__': Operator('≤', 8, lambda l, r: l.value <= r.value),
	'__gt__': Operator('≥', 8, lambda l, r: l.value >= r.value),

	'__neg__': Operator('-', 1, lambda x: -x),
	'__pos__': Operator('+', 1, lambda x: +x),
	'__invert__': Operator('~', 1, lambda x: ~x),

}
opers.update({
	'__radd__': InvertedOperator(opers['__add__']),
	'__rsub__': InvertedOperator(opers['__sub__']),
	'__rmul__': InvertedOperator(opers['__mul__']),
	'__rtruediv__': InvertedOperator(opers['__truediv__']),
	'__rfloordiv__': InvertedOperator(opers['__floordiv__']),
	'__rmod__': InvertedOperator(opers['__mod__']),
	'__rmatmul__': InvertedOperator(opers['__pow__']),
	'__rpow__': InvertedOperator(opers['__pow__']),

	'__rand__': InvertedOperator(opers['__and__']),
	'__ror__': InvertedOperator(opers['__or__']),
	'__rxor__': InvertedOperator(opers['__xor__']),
	'__rlshift__': InvertedOperator(opers['__lshift__']),
	'__rrshift__': InvertedOperator(opers['__rshift__']),
})
