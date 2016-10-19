from typing import Callable
from functools import reduce

from pymath2 import Undefined
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.named_obj import NamedObj

from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator

class Operator(UnseededFunction, NamedObj):
	seeded_type = SeededOperator
	is_inverted = False
	def __init__(self, name: str,
				 priority: int,
				 wrapped_function: Callable = Undefined,
				 req_arg_len = Undefined) -> None:
		UnseededFunction.__init__(self, wrapped_function, req_arg_len = -1)
		NamedObj.__init__(self, name)
		self.priority = priority

	@property
	def func_name(self) -> str:
		if __debug__:
			assert len([name for name, oper in opers.items() if self is oper]) == 1
		return next(name for name, oper in opers.items() if self is oper)

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		print(type(self))
		print(repr(self.wrapped_function))
		return (repr(self.wrapped_function))
		return '{}({!r}, {!r}, {!r}, {!r})'.format(type(self).__qualname__,
			self.name,
			self.priority,
			self.wrapped_function,
			self.req_arg_len)

	def is_lower_precedence(self, other: UnseededFunction) -> bool:
		if not hasattr(other, 'priority'):
			return False
		return self.priority < other.priority

	def deriv(self, du: Variable, *args: (ValuedObj, )) -> ('ValuedObj', Undefined):
		raise ValueError('What error type? TODO: find this out. But this class doesn\'t have a deriv defined: {}'.format(self.func_name))
		# return Undefined

	# def simplify(self, *args):
	# 	return None

class MultiArgOperator(Operator):

	func_for_two_args = Undefined

	def __init__(self, name: str, priority: int) -> None:
		super().__init__(name, priority, req_arg_len = -1)

	def _reduce_args(self, *args): # async
		if __debug__:
			assert args, 'dont know how to deal with 0 length args yet, but its possible'
		last_res = args[0]
		for arg in args[1:]:
			last_res = self.scrub(self.func_for_two_args(last_res, arg))
		return last_res

	@Operator.wrapped_function.getter
	def wrapped_function(self):
		if __debug__:
			assert self.func_for_two_args is not Undefined
		return self._reduce_args

class AddSubOperator(MultiArgOperator):
	def __init__(self, name: str) -> None:
		super().__init__(name, 3)
		if __debug__:
			assert name in {'+', '-'}

	# future: async lambda 
	@staticmethod
	def _lambda_plus(l, r): #async
		lv = (l.value) #future
		rv = (r.value) #future
		return lv + rv #await

	# future: async lambda 
	@staticmethod
	def _lambda_minus(l, r): #async
		lv = (l.value) #future
		rv = (r.value) #future
		return lv - rv #await

	@property
	def func_for_two_args(self):
		if self._is_plus:
			return self._lambda_plus
		return self._lambda_minus

	@property
	def _is_plus(self) -> bool:
		print('isplus')
		return self.name == '+'

	def deriv(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = (l.deriv(du)) #future
		rd = (r.deriv(du)) #future
		if self._is_plus:
			return ld + rd #await
		return ld - rd #await

class MulOperator(MultiArgOperator):
	# future: async lambda 
	@staticmethod
	def func_for_two_args(l, r): #async
		lv = (l.value) #future
		rv = (r.value) #future
		return lv * rv #await

	def __init__(self) -> None:
		super().__init__('*', 2)

	def deriv(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = (l.deriv(du)) #future
		rd = (r.deriv(du)) #future
		return ld * r + l * rd #await

class TrueDivOperator(MultiArgOperator):
	# future: async lambda 
	@staticmethod
	def func_for_two_args(l, r):
		lv = (l.value) #future
		rv = (r.value) #future
		return lv / rv #await

	# func_for_two_args = staticmethod(lambda l, r: l.value / r.value)

	def __init__(self) -> None:
		super().__init__('/', 2)

	def deriv(self, du: Variable, n: ValuedObj, d: ValuedObj) -> (ValuedObj, Undefined):
		nd = (n.deriv(du)) #future
		dd = (d.deriv(du)) #future
		return (d * nd - n * dd) / d ** 2 #await

class PowOperator(MultiArgOperator):
	# future: async lambda
	@staticmethod
	def func_for_two_args(b, p):
		bv = (b.value) #future
		pv = (p.value) #future
		return bv ** pv #await

	# func_for_two_args = staticmethod(lambda b, p: b.value ** p.value)

	def __init__(self) -> None:
		super().__init__('**', 0)

	def _reduce_args(self, *args):
		if __debug__:
			assert args, 'dont know how to deal with 0 length args yet, but its possible'
		last_res = args[-1]
		for arg in reversed(args[:-1]):
			last_res = self.scrub(self.func_for_two_args(arg, last_res)) #await
		return last_res
		# this is different for power of, but i ahvent fixed 

	def deriv(self, du: Variable, b: ValuedObj, p: ValuedObj) -> (ValuedObj, Undefined):
		bc = (b.isconst(du)) #future
		pc = (p.isconst(du)) #future
		bc = bc #await
		pc = pc #await
		if bc and pc:
			return 0

		if not bc:
			bd = (b.deriv(du)) #future
		if not pc:
			pd = (p.deriv(du)) #future
			from pymath2.extensions.functions import ln
			lnb = ln(b)

		if not bc and pc:
			return p * b ** (p - 1) * bd #await
		if bc and not pc:
			return b ** p * lnb * pd #await
		return b ** p * (bd * p / b + pd * lnb) #await

class UnaryOper(Operator):
	def __init__(self, name: str) -> None:
		super().__init__(name, 1, req_arg_len = 1)
		if __debug__:
			assert self.name in set('+-~')

	@Operator.wrapped_function.getter
	def wrapped_function(self) -> Callable:
		if self.name == '-':
			return lambda x: -x.value
		if self.name == '~':
			return lambda x: ~x.value
		return lambda x: +x.value

	def deriv(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		if __debug__:
			assert len(args) == 1
		if self.name == '-':
			return -args[0].deriv(du)
		if self.name == '+':
			return +args[0].deriv(du)
		return super().deriv(du, args)

class InvertedOperator(Operator):
	is_inverted = True
	def __init__(self, _normal_operator: Operator) -> None:
		self._normal_operator = _normal_operator
		import asyncio
		super().__init__(self._normal_operator.name,
			self._normal_operator.priority,
			req_arg_len = self._normal_operator.req_arg_len)

	@Operator.wrapped_function.getter
	def wrapped_function(self) -> Callable:
		return lambda a, b: self._normal_operator.wrapped_function(b, a)

	def deriv(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		return self._normal_operator.deriv(du, *args[::-1]) #haha! that's how you invert it

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

	'__neg__': UnaryOper('-'),
	'__pos__': UnaryOper('+'),
	'__invert__': UnaryOper('~'),
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


# future: async lambda
def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv // rv #future
opers['__floordiv__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv % rv #future
opers['__mod__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv @ rv #future
opers['__matmul__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv & rv #future
opers['__and__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv | rv #future
opers['__or__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv ^ rv #future
opers['__xor__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv << rv #future
opers['__lshift__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv >> rv #future
opers['__rshift__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv < rv #future
opers['__lt__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv > rv #future
opers['__gt__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv <= rv #future
opers['__le__']._wrapped_function = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv >= rv #future
opers['__gt__']._wrapped_function = wrap_func


def wrap_func(x): return -x.value
opers['__neg__']._wrapped_function = wrap_func

def wrap_func(x): return +x.value
opers['__pos__']._wrapped_function = wrap_func

def wrap_func(x): return ~x.value
opers['__invert__']._wrapped_function = wrap_func


del wrap_func



