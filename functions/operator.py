from typing import Callable
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
from pymath2.objs.named_obj import NamedObj
class Operator(UnseededFunction, NamedObj):
	seeded_type = seeded_operator
	def __init__(self, name: str, inp_func: Callable, is_r = False):
		UnseededFunction.__init__(self, inp_func)
		NamedObj.__init__(self, name)

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return '{}({}, {!r}{})'.format(type(self).__qualname__, self.name, self.inp_func, self.is_r or '')

opers = {
	'__add__': Operator('+', lambda l, r: l.value + r.value),
	'__sub__': Operator('-', lambda l, r: l.value - r.value),
	'__mul__': Operator('*', lambda l, r: l.value * r.value),
	'__truediv__': Operator('/', lambda l, r: l.value / r.value),
	'__floordiv__': Operator('//', lambda l, r: l.value // r.value),
	'__mod__': Operator('%', lambda l, r: l.value % r.value),
	'__pow__': Operator('**', lambda l, r: l.value ** r.value),

	'__radd__': Operator('+', lambda r, l: l.value + r.value, is_r = True),
	'__rsub__': Operator('-', lambda r, l: l.value - r.value, is_r = True),
	'__rmul__': Operator('**', lambda r, l: l.value ** r.value, is_r = True),
	'__rtruediv__': Operator('/', lambda r, l: l.value / r.value, is_r = True),
	'__rfloordiv__': Operator('//', lambda r, l: l.value // r.value, is_r = True),
	'__rmod__': Operator('%', lambda r, l: l.value % r.value, is_r = True),
	'__rpow__': Operator('**', lambda r, l: l.value ** r.value, is_r = True),

	# '__eq__': Operator('==', lambda a, b: a == b),
	# '__ne__': Operator('', lambda l, r: l.value  r.value),
	# '__lt__': Operator('+', lambda l, r: l.value + r.value),
	# '__gt__': Operator('+', lambda l, r: l.value + r.value),
	# '__le__': Operator('+', lambda l, r: l.value + r.value),
	# '__gt__': Operator('+', lambda l, r: l.value + r.value),

	'__neg__': Operator('-', lambda x: -x),
	'__pos__': Operator('=', lambda x: +x),
	'__invert__': Operator('~', lambda x: ~x),

	'__and__': Operator('&', lambda l, r: l.value & r.value),
	'__or__': Operator('|', lambda l, r: l.value | r.value),
	'__xor__': Operator('^', lambda l, r: l.value ^ r.value),
	'__lshift__': Operator('<<', lambda l, r: l.value << r.value),
	'__rshift__': Operator('>>', lambda l, r: l.value >> r.value),

	'__rand__': Operator('&', lambda r, l: l.value & r.value, is_r = True),
	'__ror__': Operator('|', lambda r, l: l.value | r.value, is_r = True),
	'__rxor__': Operator('^', lambda r, l: l.value ^ r.value, is_r = True),
	'__rlshift__': Operator('<<', lambda r, l: l.value << r.value, is_r = True),
	'__rrshift__': Operator('>>', lambda r, l: l.value >> r.value, is_r = True),

}
# 	'__add__': lambda a, b: print('add:', a, b,),
# 	'div': pymath2.functions.operator.Operator(lambda a, b: print('add:', a, b,))
# }
