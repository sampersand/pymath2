import inspect
from pymath2.objs import MathObj
import pymath2.functions.operator as oper
def _curr_func_name():
	return inspect.stack()[1][3]

class Operable(MathObj):
	def __add__(self, other):
		return oper.opers[_curr_func_name()](self, other)
