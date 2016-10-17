from typing import Any
from pymath2 import Undefined
from pymath2.builtins.objs.math_obj import MathObj
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from .seeded_function import SeededFunction
from pymath2.builtins.objs.operable import Operable
class SeededOperator(SeededFunction):
	def __init__(self, oper: 'Operator', args: tuple) -> None:
		super().__init__(oper, args)
		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base_object, Operator)

	def is_lower_precedence(self, other: SeededFunction) -> bool:
		if not hasattr(other, 'unseeded_base_object'):
			return False
		return self.unseeded_base_object.is_lower_precedence(other.unseeded_base_object) #should have because self.unseeded_base_object is an operator

	def possibly_surround_in_parens(self, other: MathObj) -> str:
		if self.is_lower_precedence(other):
			return '({})'.format(other)
		return str(other)

	def _bool_oper_str(self) -> str:
		# print('Dummy Method: _bool_oper_str')
		l = self.possibly_surround_in_parens(self.args[self.unseeded_base_object.is_inverted])
		r = self.possibly_surround_in_parens(self.args[not self.unseeded_base_object.is_inverted])
		return '{} {} {}'.format(l, self.name, r)

	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		elif self.unseeded_base_object.req_arg_len == 1:
			return '{}{}'.format(self.arg, self.possibly_surround_in_parens(self.args[0]))
		elif self.unseeded_base_object.req_arg_len == 2:
			return self._bool_oper_str()
		else:
			from pymath2.builtins.exceptions.pymath2_error import PyMath2Error
			raise PyMath2Error('How does an operator have {} required arguments?'.
								format(self.unseeded_base_object.req_arg_len))

	async def deriv(self, du: Variable) -> ('ValuedObj', Undefined):
		return await self.unseeded_base_object.deriv(du, *self.args)





















