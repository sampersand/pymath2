import inspect
from pymath2.objs.obj import obj
from pymath2.functions import opers
def _curr_func_name():
	return inspect.stack()[1][3]

class operable(object):
	def __add__(self, other):
		return opers[_curr_func_name()](self, other)
