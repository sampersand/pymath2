from typing import Any
from pymath2 import Undefined, override
from pymath2.builtins.objs.math_obj import MathObj
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from .seeded_function import SeededFunction
class SeededOperator(SeededFunction):
	@classmethod
	def _collapse_args(cls, unseeded_base_object, args, kwargs):
		if unseeded_base_object.req_arg_len == -1:
			args_to_pass = []
			do_make_new = False
			for arg in args:
				if isinstance(arg, SeededOperator) and unseeded_base_object is arg.unseeded_base_object:
					args_to_pass += arg.args
					do_make_new = True
				else:
					args_to_pass.append(arg)
			if do_make_new:
				args = args_to_pass
				# print(args_to_pass)
				# return cls(unseeded_base_object, args, **kwargs)
				return cls(unseeded_base_object= unseeded_base_object, args = args_to_pass, **kwargs)

	async def __anew__(cls, unseeded_base_object: 'Operator', args: tuple, **kwargs) -> 'SeededOperator':
		collapsed = cls._collapse_args(unseeded_base_object, args, kwargs)
		if collapsed != None:
			return collapsed
		# simplified = unseeded_base_object.simplify(cls, args, kwargs)
		# print('simplified', simplified)
		# if simplified != None:
			# return simplified
		return await super().__anew__(cls, unseeded_base_object = unseeded_base_object, args = args, **kwargs)

	@override(SeededFunction)
	async def __ainit__(self, unseeded_base_object, args, **kwargs) -> None:
		await super().__ainit__(unseeded_base_object = unseeded_base_object, args = args, **kwargs)

		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base_object, Operator)

	@override(SeededFunction)
	async def __arepr__(self) -> str:
		return '{}({}, {})'.format(self.__class__.__name__,
			(await self.async_getattr(self.unseeded_base_object))(),
			(await self.async_getattr(self.args))())


	def _is_lower_precedence(self, other: SeededFunction) -> bool:
		if not hasattr(other, 'unseeded_base_object'):
			return False
		return self.unseeded_base_object._is_lower_precedence(other.unseeded_base_object) #should have because self.unseeded_base_object is an operator

	def _possibly_surround_in_parens(self, other: MathObj) -> str:
		if self._is_lower_precedence(other):
			return '({})'.format(other)
		return str(other)


	async def _bool_oper_str(self, l, r) -> str:
		# print('Dummy Method: _bool_oper_str')
		l = self._possibly_surround_in_parens(l)
		r = self._possibly_surround_in_parens(r)
		return '{} {} {}'.format(l, await self._aname, r)

	@override(SeededFunction)
	async def __astr__(self) -> str:
		if await self._ahasvalue:
			return str(await self._avalue)
		req_arg_len = self.unseeded_base_object.req_arg_len
		if req_arg_len == 1:
			return '{}{}'.format(self._aname, self._possibly_surround_in_parens(self.args[0]))
		elif req_arg_len == 2:
			return self._bool_oper_str(*(self.args if not self.unseeded_base_object.is_inverted else self.args[::-1]))
		elif req_arg_len == -1:
			async def func_to_reduce(a, b):
				return await self._bool_oper_str(a, b)
			ret = self.async_getattr(await func_to_reduce(self.args[0], self.args[1]), '__str__')
			for a in self.args[2:]:
				ret = func_to_reduce(ret, a)
			return ret
		else:
			raise Exception('How does an operator have {} required arguments?'.
								format(self.unseeded_base_object.req_arg_len))

	@override(SeededFunction)
	async def _aderiv(self, du: Variable) -> ('ValuedObj', Undefined):
		return await self.unseeded_base_object.deriv_w_args(du, *self.args) #await





















