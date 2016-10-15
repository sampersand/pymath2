import inspect
from .math_obj import MathObj
def _curr_func_name():
	return inspect.stack()[1][3]
class Operable(MathObj):
	def __add__(self, other):
		from pymath2.functions.operator import opers
		return opers[_curr_func_name()](self, other)
