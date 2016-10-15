import inspect
from . import obj
from pymath2.functions import opers
def _curr_func_name():
	return inspect.stack()[1][3]

class operable(obj):
	def __add__(self, other):
		return opers[_curr_func_name()](self, other)
