from typing import Any
from pymath2.objs.named_valued_obj import NamedValuedObj
from pymath2.objs.operable import Operable
from .operator import Operator
class SeededOperator(SeededFunction):
	def __init__(self, uns_func: 'Operator', args: tuple) -> None:
		super().__init__(uns_func, args)
		if __debug__:
			assert isinstance(uns_func, Operator)
	def possibly_surround_in_parents(self, arg):
		print('Dummy Method: possibly_surround_in_parents')
		return arg.str
	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		if self.uns_func.arg_count == 1:
			return '{}{}'.format(self.arg, self.possibly_surround_in_parents(self.args[0]))

