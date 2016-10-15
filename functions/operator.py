from typing import Callable
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
from pymath2.objs.named_obj import NamedObj
class Operator(UnseededFunction, NamedObj):
	seeded_type = SeededOperator
	def __init__(self, name: str, priority: int, callable_: Callable) -> None:
		UnseededFunction.__init__(self, callable_)
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
		return '{}({!r}, {!r}, {!r})'.format(type(self).__qualname__, self.name, self.priority, self.callable_)

	def is_lower_precedence(self, other: UnseededFunction) -> bool:
		pass
class InvertedOperator(Operator):
	def __init__(self, normal_operator: Operator) -> None:
		pass
		# super().__init__(normal_operator.name, normal_operator.priority, normal_operator.)

opers = {
	'__add__': Operator('+', lambda l, r: l.value + r.value),
	'__sub__': Operator('-', lambda l, r: l.value - r.value),
	'__mul__': Operator('*', lambda l, r: l.value * r.value),
	'__truediv__': Operator('/', lambda l, r: l.value / r.value),
	'__floordiv__': Operator('//', lambda l, r: l.value // r.value),
	'__mod__': Operator('%', lambda l, r: l.value % r.value),
	'__pow__': Operator('**', 0, lambda l, r: l.value ** r.value),

	'__and__': Operator('&', lambda l, r: l.value & r.value),
	'__or__': Operator('|', lambda l, r: l.value | r.value),
	'__xor__': Operator('^', lambda l, r: l.value ^ r.value),
	'__lshift__': Operator('<<', lambda l, r: l.value << r.value),
	'__rshift__': Operator('>>', lambda l, r: l.value >> r.value),

	# '__eq__': Operator('==', lambda a, b: a == b),
	# '__ne__': Operator('', lambda l, r: l.value  r.value),
	'__lt__': Operator('<', lambda l, r: l.value < r.value),
	'__gt__': Operator('>', lambda l, r: l.value > r.value),
	'__le__': Operator('≤', lambda l, r: l.value <= r.value),
	'__gt__': Operator('≥', lambda l, r: l.value >= r.value),

	'__neg__': Operator('-', lambda x: -x),
	'__pos__': Operator('+', lambda x: +x),
	'__invert__': Operator('~', lambda x: ~x),

}
opers.update({
	'__radd__': InvertedOperator(opers['__radd__']),
	'__rsub__': InvertedOperator(opers['__rsub__']),
	'__rmul__': InvertedOperator(opers['__rmul__']),
	'__rtruediv__': InvertedOperator(opers['__rtruediv__']),
	'__rfloordiv__': InvertedOperator(opers['__rfloordiv__']),
	'__rmod__': InvertedOperator(opers['__rmod__']),
	'__rpow__': InvertedOperator(opers['__rpow__']),

	'__rand__': InvertedOperator(opers['__rand__']),
	'__ror__': InvertedOperator(opers['__ror__']),
	'__rxor__': InvertedOperator(opers['__rxor__']),
	'__rlshift__': InvertedOperator(opers['__rlshift__']),
	'__rrshift__': InvertedOperator(opers['__rrshift__']),
})
