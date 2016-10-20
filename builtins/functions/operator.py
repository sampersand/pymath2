from typing import Callable

from pymath2 import Undefined, Override
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.valued_obj import ValuedObj

from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator

class Operator(UnseededFunction):
	seeded_type = SeededOperator #@Override UnseededFunction
	is_inverted = False

	@Override(UnseededFunction)
	def __init__(self, priority: int, **kwargs) -> None:
		super().__init__(**kwargs)
		if __debug__:
			assert priority is not Undefined
		self.priority = priority

	@property
	def func_name(self) -> str:
		if __debug__:
			assert len([name for name, oper in opers.items() if self is oper]) == 1
		return next(name for name, oper in opers.items() if self is oper)

	@Override(UnseededFunction)
	def __str__(self) -> str:
		return self.name

	@Override(UnseededFunction)
	def __repr__(self) -> str:
		return '{}({!r}, {!r}, {!r}, {!r})'.format(self.__class__.__name__,
			self.name,
			self.priority,
			'bizarre, wrapped function...',
			# self.func,
			self.req_arg_len)

	def _is_lower_precedence(self, other: UnseededFunction) -> bool: #_NOT_ the same as the one in SeededFunction
		if not hasattr(other, 'priority'):
			return False
		return self.priority < other.priority

	def deriv_w_args(self, du: Variable, *args: (ValuedObj, )) -> (ValuedObj, Undefined):
		raise NotImplementedError

	# def simplify(self, *args):
	# 	return None

class MultiArgOperator(Operator):

	func_for_two_args = Undefined

	@Override(Operator)
	def __init__(self, *args, **kwargs) -> None:
		return super().__init__(req_arg_len = -1, **kwargs)

	def _reduce_args(self, *args): # async
		if __debug__:
			assert args, 'dont know how to deal with 0 length args yet, but its possible'
		last_res = args[0]
		for arg in args[1:]:
			last_res = self.scrub(self.func_for_two_args(last_res, arg))
		return last_res

	# @Override(Operator)
	# __func = UnseededFunction.func
	# @Operator.func.getter
	@property
	def func(self):
		if __debug__:
			assert self.func_for_two_args is not Undefined
		return self._reduce_args
	@func.setter
	def func(self, val):
		pass
	# func = property(fget = func, fset = __func.fset)

class AddSubOperator(MultiArgOperator):
	@Override(MultiArgOperator)
	def __init__(self, name: str, **kwargs) -> None:
		super().__init__(name = name, priority = 3, **kwargs)
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

	@Override(MultiArgOperator)
	@property
	def func_for_two_args(self):
		if self._is_plus:
			return self._lambda_plus
		return self._lambda_minus

	@property
	def _is_plus(self) -> bool:
		return self.name == '+'

	@Override(MultiArgOperator)
	def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = (l.deriv(du)) #future
		rd = (r.deriv(du)) #future
		if self._is_plus:
			return ld + rd #await
		return ld - rd #await

class MulOperator(MultiArgOperator):

	@Override(MultiArgOperator)
	def __init__(self, **kwargs) -> None:
		super().__init__(name = '*', priority = 2, **kwargs)

	@Override(MultiArgOperator)
	@staticmethod
	def func_for_two_args(l, r): #async
		lv = (l.value) #future
		rv = (r.value) #future
		return lv * rv #await

	@Override(MultiArgOperator)
	def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = (l.deriv(du)) #future
		rd = (r.deriv(du)) #future
		return ld * r + l * rd #await

class TrueDivOperator(MultiArgOperator):

	@Override(MultiArgOperator)
	def __init__(self, **kwargs) -> None:
		super().__init__(name = '/', priority = 2, **kwargs)

	@Override(MultiArgOperator)
	@staticmethod
	def func_for_two_args(l, r):
		lv = (l.value) #future
		rv = (r.value) #future
		return lv / rv #await

	@Override(MultiArgOperator)
	def deriv_w_args(self, du: Variable, n: ValuedObj, d: ValuedObj) -> (ValuedObj, Undefined):
		nd = (n.deriv(du)) #future
		dd = (d.deriv(du)) #future
		return (d * nd - n * dd) / d ** 2 #await

class PowOperator(MultiArgOperator):

	@Override(MultiArgOperator)
	def __init__(self, **kwargs) -> None:
		super().__init__(name = '**', priority = 0, **kwargs)

	@Override(MultiArgOperator)
	@staticmethod
	def func_for_two_args(b, p):
		bv = (b.value) #future
		pv = (p.value) #future
		return bv ** pv #await


	@Override(MultiArgOperator)
	def _reduce_args(self, *args):
		if __debug__:
			assert args, 'dont know how to deal with 0 length args yet, but its possible'
		last_res = args[-1]
		for arg in reversed(args[:-1]):
			last_res = self.scrub(self.func_for_two_args(arg, last_res)) #await
		return last_res
		# this is different for power of, but i ahvent fixed 

	@Override(MultiArgOperator)
	def deriv_w_args(self, du: Variable, b: ValuedObj, p: ValuedObj) -> (ValuedObj, Undefined):
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
	@Override(Operator)
	def __init__(self, **kwargs) -> None:
		super().__init__(priority = 1, req_arg_len = 1, **kwargs)
		if __debug__:
			assert self.name in set('+-~')

	@Override(Operator)
	@Operator.func.getter
	def func(self) -> Callable:
		if self.name == '-':
			return lambda x: -x.value
		if self.name == '~':
			return lambda x: ~x.value
		return lambda x: +x.value

	@Override(Operator)
	def deriv_w_args(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		if __debug__:
			assert len(args) == 1
		if self.name == '-':
			return -args[0].deriv(du)
		if self.name == '+':
			return +args[0].deriv(du)
		return super().deriv_w_args(self, du, *args)

class InvertedOperator(Operator):
	is_inverted = True
	@Override(Operator)
	def __init__(self, _normal_operator: Operator, **kwargs) -> None:

		self._normal_operator = _normal_operator

		if __debug__:
			assert 'name' not in kwargs
			assert 'priority' not in kwargs
			assert 'req_arg_len' not in kwargs

		super().__init__(name = self._normal_operator.name,
						 priority = self._normal_operator.priority,
						 req_arg_len = self._normal_operator.req_arg_len,
						 **kwargs)
	@Override(Operator)
	@Operator.func.getter
	def func(self) -> Callable:
		return lambda a, b: self._normal_operator.func(b, a)

	@Override(Operator)
	def deriv_w_args(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		return self._normal_operator.deriv_w_args(du, *args[::-1]) #haha! that's how you invert it

opers = {
	'__add__': AddSubOperator(name = '+'),
	'__sub__': AddSubOperator(name = '-'),
	'__mul__': MulOperator(),
	'__truediv__': TrueDivOperator(),
	'__floordiv__': Operator(name = '//', priority = 2, func = lambda l, r: l.value // r.value),
	'__mod__': Operator(name = '%', priority = 2, func = lambda l, r: l.value % r.value),
	'__matmul__': Operator(name = '@', priority = 2, func = lambda l, r: l.value @ r.value),
	'__pow__': PowOperator(),

	'__and__': Operator(name = '&', priority = 5, func = lambda l, r: l.value & r.value),
	'__or__': Operator(name = '|', priority = 7, func = lambda l, r: l.value | r.value),
	'__xor__': Operator(name = '^', priority = 6, func = lambda l, r: l.value ^ r.value),
	'__lshift__': Operator(name = '<<',priority =  4, func = lambda l, r: l.value << r.value),
	'__rshift__': Operator(name = '>>',priority =  4, func = lambda l, r: l.value >> r.value),

	# '__eq__': Operator('==', lambda a, b: a == b),
	# '__ne__': Operator('', lambda l, r: l.value  r.value),
	'__lt__': Operator(name = '<', priority = 8, func = lambda l, r: l.value < r.value),
	'__gt__': Operator(name = '>', priority = 8, func = lambda l, r: l.value > r.value),
	'__le__': Operator(name = '≤', priority = 8, func = lambda l, r: l.value <= r.value),
	'__gt__': Operator(name = '≥', priority = 8, func = lambda l, r: l.value >= r.value),

	'__neg__': UnaryOper(name = '-'),
	'__pos__': UnaryOper(name = '+'),
	'__invert__': UnaryOper(name = '~'),
}

opers.update({
	'__radd__': InvertedOperator(_normal_operator = opers['__add__']),
	'__rsub__': InvertedOperator(_normal_operator = opers['__sub__']),
	'__rmul__': InvertedOperator(_normal_operator = opers['__mul__']),
	'__rtruediv__': InvertedOperator(_normal_operator = opers['__truediv__']),
	'__rfloordiv__': InvertedOperator(_normal_operator = opers['__floordiv__']),
	'__rmod__': InvertedOperator(_normal_operator = opers['__mod__']),
	'__rmatmul__': InvertedOperator(_normal_operator = opers['__pow__']),
	'__rpow__': InvertedOperator(_normal_operator = opers['__pow__']),

	'__rand__': InvertedOperator(_normal_operator = opers['__and__']),
	'__ror__': InvertedOperator(_normal_operator = opers['__or__']),
	'__rxor__': InvertedOperator(_normal_operator = opers['__xor__']),
	'__rlshift__': InvertedOperator(_normal_operator = opers['__lshift__']),
	'__rrshift__': InvertedOperator(_normal_operator = opers['__rshift__']),
})


# future: async lambda
def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv // rv #future
opers['__floordiv__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv % rv #future
opers['__mod__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv @ rv #future
opers['__matmul__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv & rv #future
opers['__and__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv | rv #future
opers['__or__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv ^ rv #future
opers['__xor__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv << rv #future
opers['__lshift__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv >> rv #future
opers['__rshift__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv < rv #future
opers['__lt__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv > rv #future
opers['__gt__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv <= rv #future
opers['__le__']._func = wrap_func

def wrap_func(l, r): lv, rv = (l.value), (r.value); return lv >= rv #future
opers['__gt__']._func = wrap_func


def wrap_func(x): return -x.value
opers['__neg__']._func = wrap_func

def wrap_func(x): return +x.value
opers['__pos__']._func = wrap_func

def wrap_func(x): return ~x.value
opers['__invert__']._func = wrap_func


del wrap_func



