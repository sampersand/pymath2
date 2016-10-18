from typing import Any
from pymath2 import Undefined, await_result
from pymath2.builtins.objs.math_obj import MathObj
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from .seeded_function import SeededFunction
from pymath2.builtins.objs.operable import Operable
class SeededOperator(SeededFunction):
	@staticmethod
	def _consolidate_args(args):
		ret = args
		# if __debug__:
		# if not hasattr(other, 'unseeded_base_object'):
		# print('args0:', args[0])
		return ret
	def __init__(self, oper: 'Operator', args: tuple) -> None:
		super().__init__(oper, self._consolidate_args(args))
		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base_object, Operator)

	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(type(self).__qualname__, self.unseeded_base_object, self.args)

	def is_lower_precedence(self, other: SeededFunction) -> bool:
		if not hasattr(other, 'unseeded_base_object'):
			return False
		return self.unseeded_base_object.is_lower_precedence(other.unseeded_base_object) #should have because self.unseeded_base_object is an operator

	def possibly_surround_in_parens(self, other: MathObj) -> str:
		if self.is_lower_precedence(other):
			return '({})'.format(other)
		return str(other)


	def _bool_oper_str(self, l, r) -> str:
		# print('Dummy Method: _bool_oper_str')
		l = self.possibly_surround_in_parens(l)
		r = self.possibly_surround_in_parens(r)
		return '{} {} {}'.format(l, self.name, r)

	def __str__(self) -> str:
		if await_result(self.hasvalue):
			return str(self.value)
		elif self.unseeded_base_object.req_arg_len == 1:
			return '{}{}'.format(self.name, self.possibly_surround_in_parens(self.args[0]))
		elif self.unseeded_base_object.req_arg_len == 2:
			return self._bool_oper_str(*(self.args if not self.unseeded_base_object.is_inverted else self.args[::-1]))
		elif self.unseeded_base_object.req_arg_len == -1:
			from functools import reduce
			return reduce(lambda a, b: self._bool_oper_str(a, b), self.args)
		else:
			from pymath2.builtins.exceptions.pymath2_error import PyMath2Error
			raise PyMath2Error('How does an operator have {} required arguments?'.
								format(self.unseeded_base_object.req_arg_len))

	async def deriv(self, du: Variable) -> ('ValuedObj', Undefined):
		return await self.unseeded_base_object.deriv(du, *self.args)





















