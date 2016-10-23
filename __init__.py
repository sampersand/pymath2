_complete_by_default = True
def enable_complete():
	# print('enabled!')
	global _complete_by_default
	_complete_by_default = True
def disable_complete():
	# print('disabled!')
	global _complete_by_default
	_complete_by_default = False
def do_complete():
	# print('do_complete:!', _complete_by_default)
	return _complete_by_default
import asyncio
_global_loops = []
def add_global_loop():
	global _global_loops
	print('added _global_loops')
	_global_loops.append(asyncio.new_event_loop())
def remove_global_loop():
	global _global_loops
	del _global_loops[-1]
	print('removed _global_loops')
	assert _global_loops
def get_global_loop():
	print('_global_loops', _global_loops)
	if not _global_loops:
		return asyncio.get_event_loop()
	return _global_loops[-1]


from .utils import *
from .builtins.undefined import Undefined
from .builtins.constant import Constant, UserConstant as const
from .builtins.variable import Variable, UserVariable as var
from .builtins.derivative import Derivative, UserDerivative as d
from .builtins.functions.unseeded_function import UnseededFunction, UserFunction as func
# from .extensions import *

from .builtins.functions.operator import opers
del opers




__all__ = tuple(x for x in tuple(locals()) if x[0] != '_')