from typing import Callable
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

opers = {
	'__add__': Operator('+', 3, lambda l, r: l.value + r.value),
	'__sub__': Operator('-', 3, lambda l, r: l.value - r.value),
	'__mul__': Operator('*', 2, lambda l, r: l.value * r.value),
	'__truediv__': Operator('/', 2, lambda l, r: l.value / r.value),
	'__floordiv__': Operator('//', 2, lambda l, r: l.value // r.value),
	'__mod__': Operator('%', 2, lambda l, r: l.value % r.value),
	'__matmul__': Operator('@', 2, lambda l, r: l.value @ r.value),
	'__pow__': Operator('**', 0, lambda l, r: l.value ** r.value),

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
