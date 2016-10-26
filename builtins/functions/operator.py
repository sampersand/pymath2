from typing import Callable

from pymath2 import Undefined, override, complete, ensure_future, finish
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.math_obj import MathObj
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
async def _domethod(funcname, l, *args):
	if await MathObj.has_asyncattr(l, funcname):
		attr = await l.get_asyncattr(l, funcname, call = False)
		called_attr = attr(*args)
		return await called_attr
		# return await (await l.get_asyncattr(funcname, call = False))(*args)
	return getattr(l, funcname)(*args)

class Operator(UnseededFunction):
	seeded_type = SeededOperator #@override UnseededFunction
	is_inverted = False

	@override(UnseededFunction)
	async def __ainit__(self, priority: int, **kwargs) -> None:
		assert priority is not Undefined

		ainit = ensure_future(super().__ainit__(**kwargs))
		aprop = ensure_future(self.__asetattr__('priority', priority))
		await ainit
		await aprop

	@property
	def func_name(self) -> str:
		ret = [name for name, oper in opers.items() if self is oper]
		assert len(ret) == 1

		return next(ret)

	@override(UnseededFunction)
	async def __astr__(self) -> str:
		return await self._aname

	@override(UnseededFunction)
	async def __arepr__(self) -> str:
		return '{}({}, {}, {}, {})'.format(self.__class__.__name__,
			await self._aname,
			self.priority,
			'bizarre, wrapped function...',
			# self.func,
			self.req_arg_len)

	async def _is_lower_precedence(self, other: UnseededFunction) -> bool: #_NOT_ the same as the one in SeededFunction
		if not await self._ahasattr(other, 'priority'): #what is this
			return False
		return self.priority < other.priority

	async def deriv_w_args(self, du: Variable, *args: (ValuedObj, )) -> (ValuedObj, Undefined):
		raise NotImplementedError


	def simplify(self, *args):
		return None

class MultiArgOperator(Operator):

	func_for_two_args = Undefined


	@override(Operator)
	async def __ainit__(self, *args, **kwargs) -> None:
		await super().__ainit__(req_arg_len = -1, **kwargs)

	async def _reduce_args(self, *args): # async
		assert args, 'dont know how to deal with 0 length args yet, but its possible'

		last_res = args[0]
		for arg in args[1:]:
			val = await self.func_for_two_args(last_res, arg)
			last_res = await self.scrub(val)
		return last_res

	# __func = UnseededFunction.func
	# @Operator.func.getter
	@override(Operator)
	@property
	async def _afunc(self):
		assert self.func_for_two_args is not Undefined

		return self._reduce_args

	@override(Operator)
	async def _afunc_setter(self, val):
		pass
	# func = property(fget = func, fset = __func.fset)

class SubOperator(MultiArgOperator):
	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '-', priority = 3, **kwargs)

	@staticmethod
	async def func_for_two_args(l, r):
		lv = ensure_future(l._avalue)
		rv = ensure_future(r._avalue)
		return await _domethod('__sub__', await lv, await rv)

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = ensure_future(l._aderiv(du))
		rd = ensure_future(r._aderiv(du))
		return await ld - await rd


	@override(Operator)
	def simplify(self, cls, args, kwargs_to_pass):
		args = list(args)
		# print(args)
		if not any(x == 0 for x in args):
			return None
		assert False, 'todo'
		# for i in range(len(args)):
		# 	if args[i] == 0:
		# 		args.pop(i)
		# return cls(self, args, **kwargs_to_pass)

class AddOperator(MultiArgOperator):
	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '+', priority = 3, **kwargs)

	@staticmethod
	async def func_for_two_args(l, r):
		assert r is not None
		lv = ensure_future(l._avalue)
		rv = ensure_future(r._avalue)
		return await _domethod('__add__', await lv, await rv)

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = ensure_future(l._aderiv(du))
		rd = ensure_future(r._aderiv(du))
		return await ld + await rd


	@override(Operator)
	def simplify(self, cls, args, kwargs_to_pass):
		args = list(args)
		# print(args)
		if not any(x == 0 for x in args):
			return None
		for i in range(len(args)):
			if args[i] == 0:
				args.pop(i)
		return cls(self, args, **kwargs_to_pass)


class MulOperator(MultiArgOperator):

	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '*', priority = 2, **kwargs)

	@override(MultiArgOperator)
	@staticmethod
	async def func_for_two_args(l, r): #async
		lv = ensure_future(l._avalue)
		rv = ensure_future(r._avalue)
		return await _domethod('__mul__', await lv, await rv)

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = ensure_future(l._aderiv(du))
		rd = ensure_future(r._aderiv(du))
		return await ld * r + l * await rd 

class TrueDivOperator(MultiArgOperator):

	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '/', priority = 2, **kwargs)

	@override(MultiArgOperator)
	@staticmethod
	async def func_for_two_args(l, r):
		lv = ensure_future(l._avalue)
		rv = ensure_future(r._avalue)
		return await _domethod('__truediv__', await lv, await rv)

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, n: ValuedObj, d: ValuedObj) -> (ValuedObj, Undefined):
		nd = ensure_future(n._aderiv(du))
		dd = ensure_future(d._aderiv(du))
		return (d * await nd - n * await dd) / d ** 2

class PowOperator(MultiArgOperator):

	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '**', priority = 0, **kwargs)

	@override(MultiArgOperator)
	@staticmethod
	async def func_for_two_args(b, p):
		bv = ensure_future(b._avalue)
		pv = ensure_future(p._avalue)
		return await bv ** await pv


	@override(MultiArgOperator)
	async def _reduce_args(self, *args):
		assert args, 'dont know how to deal with 0 length args yet, but its possible'

		last_res = args[-1]
		for arg in reversed(args[:-1]):
			last_res = await self.scrub(await self.func_for_two_args(arg, last_res)) #await
		return last_res
		# this is different for power of, but i ahvent fixed 

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, b: ValuedObj, p: ValuedObj) -> (ValuedObj, Undefined):
		async with finish() as f:
			bc = f.future(b._aisconst(du))
			pc = f.future(p._aisconst(du))
		bc = bc.result()
		pc = pc.result()
		if bc and pc:
			return 0

		if not bc:
			bd = ensure_future(b._aderiv(du))
		if not pc:
			pd = ensure_future(p._aderiv(du))
			from pymath2.extensions.functions import ln
			lnb = await ln.__acall__(b)

		if not bc and pc:

			return p * b ** (p - 1) * await bd
		if bc and not pc:
			return b ** p * lnb * await pd
		return b ** p * (await bd * p / b + await pd * lnb)

class UnaryOper(Operator):
	@override(Operator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(priority = 1, req_arg_len = 1, **kwargs)

		assert await self._aname in set('+-~')

	@staticmethod
	async def _lambda_add(a):
		return +await x._avalue
	@staticmethod
	async def _lambda_sub(a):
		return -await x._avalue
	@staticmethod
	async def _lambda_invert(a):
		return ~await x._avalue

	@override(Operator)
	@property
	async def _afunc(self) -> Callable:
		name = await self._aname
		if name == '-':
			return self._lambda_sub
		if name == '~':
			return self._lambda_invert
		return self._lambda_add

	@override(Operator)
	async def deriv_w_args(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		assert len(args) == 1

		name = ensure_future(self._aname)
		deriv = ensure_future(args[0]._aderiv(du))
		name = await name

		if name == '-':
			return -await deriv
		if name == '+':
			return +await deriv

		return await super().deriv_w_args(self, du, *args)

class InvertedOperator(Operator):
	is_inverted = True
	@override(Operator)
	async def __ainit__(self, _normal_operator: Operator, **kwargs) -> None:
		assert 'name' not in kwargs
		assert 'priority' not in kwargs
		assert 'req_arg_len' not in kwargs

		anorm = ensure_future(self.__asetattr__('_normal_operator', _normal_operator))
		ainit = ensure_future(super().__ainit__(name = await _normal_operator._aname,
						 priority = _normal_operator.priority,
						 req_arg_len = _normal_operator.req_arg_len,
						 **kwargs))
		await anorm
		await ainit

	@override(Operator)
	@property
	async def _afunc(self) -> Callable:
		callme = await self.get_asyncattr(await self._normal_operator._afunc, '__call__')
		return lambda a, b: callme(b, a)

	@override(Operator)
	async def deriv_w_args(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		return await self._normal_operator.deriv_w_args(du, *args[::-1]) #haha! that's how you invert it

opers = {}
async def main():
	global opers
	opers = {
		'__aadd__': await AddOperator.__anew__(AddOperator),
		'__asub__': await SubOperator.__anew__(SubOperator),
		'__amul__': await MulOperator.__anew__(MulOperator, ),
		'__atruediv__': await TrueDivOperator.__anew__(TrueDivOperator, ),
		'__afloordiv__': await Operator.__anew__(Operator, name = '//', priority = 2, func = lambda l, r: l.value // r.value),
		'__amod__': await Operator.__anew__(Operator, name = '%', priority = 2, func = lambda l, r: l.value % r.value),
		'__amatmul__': await Operator.__anew__(Operator, name = '@', priority = 2, func = lambda l, r: l.value @ r.value),
		'__apow__': await PowOperator.__anew__(PowOperator, ),

		'__aand__': await Operator.__anew__(Operator, name = '&', priority = 5, func = lambda l, r: l.value & r.value),
		'__aor__': await Operator.__anew__(Operator, name = '|', priority = 7, func = lambda l, r: l.value | r.value),
		'__axor__': await Operator.__anew__(Operator, name = '^', priority = 6, func = lambda l, r: l.value ^ r.value),
		'__alshift__': await Operator.__anew__(Operator, name = '<<',priority =  4, func = lambda l, r: l.value << r.value),
		'__arshift__': await Operator.__anew__(Operator, name = '>>',priority =  4, func = lambda l, r: l.value >> r.value),

		# '__eq__': await Operator.__anew__(Operator, '==', lambda a, b: a == b),
		# '__ne__': await Operator.__anew__(Operator, '', lambda l, r: l.value  r.value),
		'__alt__': await Operator.__anew__(Operator, name = '<', priority = 8, func = lambda l, r: l.value < r.value),
		'__agt__': await Operator.__anew__(Operator, name = '>', priority = 8, func = lambda l, r: l.value > r.value),
		'__ale__': await Operator.__anew__(Operator, name = '≤', priority = 8, func = lambda l, r: l.value <= r.value),
		'__agt__': await Operator.__anew__(Operator, name = '≥', priority = 8, func = lambda l, r: l.value >= r.value),

		'__aneg__': await UnaryOper.__anew__(UnaryOper, name = '-'),
		'__apos__': await UnaryOper.__anew__(UnaryOper, name = '+'),
		'__ainvert__': await UnaryOper.__anew__(UnaryOper, name = '~'),
	}

	opers.update({
		'__aradd__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__aadd__']),
		'__arsub__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__asub__']),
		'__armul__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__amul__']),
		'__artruediv__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__atruediv__']),
		'__arfloordiv__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__afloordiv__']),
		'__armod__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__amod__']),
		'__armatmul__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__apow__']),
		'__arpow__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__apow__']),

		'__arand__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__aand__']),
		'__aror__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__aor__']),
		'__arxor__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__axor__']),
		'__arlshift__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__alshift__']),
		'__arrshift__': await InvertedOperator.__anew__(InvertedOperator, _normal_operator = opers['__arshift__']),
	})


	# ensure_future: async lambda
	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__floordiv__', await lv, await rv)
	await opers['__afloordiv__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__mod__', await lv, await rv)
	await opers['__amod__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__matmul__', await lv, await rv)
	await opers['__amatmul__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__and__', await lv, await rv)
	await opers['__aand__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__or__', await lv, await rv)
	await opers['__aor__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__xor__', await lv, await rv)
	await opers['__axor__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__lshift__', await lv, await rv)
	await opers['__alshift__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__rshift__', await lv, await rv)
	await opers['__arshift__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__lt__', await lv, await rv)
	await opers['__alt__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__gt__', await lv, await rv)
	await opers['__agt__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__le__', await lv, await rv)
	await opers['__ale__']._afunc_setter(wrap_func)

	async def wrap_func(l, r):
		lv, rv = ensure_future(l.value), ensure_future(r.value)
		return await _domethod('__gt__', await lv, await rv)
	await opers['__agt__']._afunc_setter(wrap_func)


	async def wrap_func(x):
		return await _domethod('__neg__', await x._avalue)
	await opers['__aneg__']._afunc_setter(wrap_func)

	async def wrap_func(x):
		return await _domethod('__pos__', await x._avalue)
	await opers['__apos__']._afunc_setter(wrap_func)

	async def wrap_func(x):
		return await _domethod('__invert__', await x._avalue)
	await opers['__ainvert__']._afunc_setter(wrap_func)

complete(main())