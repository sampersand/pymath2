from typing import Callable

from pymath2 import Undefined, override, complete
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.valued_obj import ValuedObj

from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator

class Operator(UnseededFunction):
	seeded_type = SeededOperator #@override UnseededFunction
	is_inverted = False

	@override(UnseededFunction)
	async def __ainit__(self, priority: int, **kwargs) -> None:
		assert priority is not Undefined

		await super().__ainit__(**kwargs)
		self.priority = priority

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

	def _is_lower_precedence(self, other: UnseededFunction) -> bool: #_NOT_ the same as the one in SeededFunction
		if not hasattr(other, 'priority'):
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
			print(await self._aname, type(self.func_for_two_args))
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

class AddOperator(MultiArgOperator):
	@override(MultiArgOperator)
	async def __ainit__(self, name: str, **kwargs) -> None:
		assert name in {'+', '-'}

		await super().__ainit__(name = name, priority = 3, **kwargs)

	@staticmethod
	async def _lambda_plus(l, r):
		lv = future(l._avalue)
		rv = future(r._avalue)
		return await lv + await rv

	@staticmethod
	async def _lambda_minus(l, r):
		lv = future(l._avalue)
		rv = future(r._avalue)
		return await lv - await rv

	@override(MultiArgOperator)
	@property
	async def func_for_two_args(self):
		if await self._ais_plus:
			return self._lambda_plus
		return self._lambda_minus

	@property
	async def _ais_plus(self) -> bool:
		return await self._aname == '+'

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = future(l.deriv(du))
		rd = future(r.deriv(du))
		if await self._ais_plus:
			return await ld + await rd
		return await ld - await rd


	@override(Operator)
	def simplify(self, cls, args, kwargs_to_pass):
		args = list(args)
		# print(args)
		if not any(x == 0 for x in args):
			return None
		if self._ais_plus:
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
		lv = future(l._avalue)
		rv = future(r._avalue)
		return await lv * await rv

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, l: ValuedObj, r: ValuedObj) -> (ValuedObj, Undefined):
		ld = future(l.deriv(du))
		rd = future(r.deriv(du))
		return await ld * r + l * await rd 

class TrueDivOperator(MultiArgOperator):

	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '/', priority = 2, **kwargs)

	@override(MultiArgOperator)
	@staticmethod
	async def func_for_two_args(l, r):
		lv = future(l._avalue)
		rv = future(r._avalue)
		return await lv / await rv

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, n: ValuedObj, d: ValuedObj) -> (ValuedObj, Undefined):
		nd = future(n.deriv(du))
		dd = future(d.deriv(du))
		return (d * await nd - n * await dd) / d ** 2

class PowOperator(MultiArgOperator):

	@override(MultiArgOperator)
	async def __ainit__(self, **kwargs) -> None:
		await super().__ainit__(name = '**', priority = 0, **kwargs)

	@override(MultiArgOperator)
	@staticmethod
	async def func_for_two_args(b, p):
		bv = future(b.value)
		pv = future(p.value)
		return await bv ** await pv


	@override(MultiArgOperator)
	async def _reduce_args(self, *args):
		assert args, 'dont know how to deal with 0 length args yet, but its possible'

		last_res = args[-1]
		for arg in reversed(args[:-1]):
			last_res = await self.scrub(self.func_for_two_args(arg, last_res)) #await
		return last_res
		# this is different for power of, but i ahvent fixed 

	@override(MultiArgOperator)
	async def deriv_w_args(self, du: Variable, b: ValuedObj, p: ValuedObj) -> (ValuedObj, Undefined):
		bc = future(b.isconst(du))
		pc = future(p.isconst(du))
		bc = await bc
		pc = await pc
		if bc and pc:
			return 0

		if not bc:
			bd = future(b.deriv(du))
		if not pc:
			pd = future(p.deriv(du))
			from pymath2.extensions.functions import ln
			lnb = ln(b)

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

		name = future(self._aname)
		deriv = future(args[0].deriv(du))
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

		self._normal_operator = _normal_operator
		await super().__ainit__(name = await self._normal_operator._aname,
						 priority = self._normal_operator.priority,
						 req_arg_len = self._normal_operator.req_arg_len,
						 **kwargs)
	@override(Operator)
	@property
	async def _afunc(self) -> Callable:
		callme = await self.async_getattr(await self._normal_operator._afunc, '__call__')
		return lambda a, b: callme(b, a)

	@override(Operator)
	async def deriv_w_args(self, du: Variable, *args: [ValuedObj]) -> (ValuedObj, Undefined):
		return await self._normal_operator.deriv_w_args(du, *args[::-1]) #haha! that's how you invert it

opers = {}
async def main():
	global opers
	opers = {
		'__aadd__': await AddSubOperator.__anew__(AddSubOperator, name = '+'),
		'__asub__': await AddSubOperator.__anew__(AddSubOperator, name = '-'),
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


	# future: async lambda
	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv // await rv
	await opers['__afloordiv__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv % await rv
	await opers['__amod__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv @ await rv
	await opers['__amatmul__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv & await rv
	await opers['__aand__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv | await rv
	await opers['__aor__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv ^ await rv
	await opers['__axor__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv << await rv
	await opers['__alshift__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv >> await rv
	await opers['__arshift__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv < await rv
	await opers['__alt__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv > await rv
	await opers['__agt__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv <= await rv
	await opers['__ale__']._afunc_setter(wrap_func)

	async def wrap_func(l, r): lv, rv = future(l.value), future(r.value); return await lv >= await rv
	await opers['__agt__']._afunc_setter(wrap_func)


	def wrap_func(x): return -x.value
	await opers['__aneg__']._afunc_setter(wrap_func)

	def wrap_func(x): return +x.value
	await opers['__apos__']._afunc_setter(wrap_func)

	def wrap_func(x): return ~x.value
	await opers['__ainvert__']._afunc_setter(wrap_func)

complete(main())


