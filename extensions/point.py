from typing import Final
from pymath2 import Undefined
from .math_list import MathList
from pymath2.builtins.objs.user_obj import UserObj
class AbstractPoint(MathList):
	print_parens = ('(', ')')

	_len_attrs = {
		2: MathList._gen_len_attr(*tuple('xy')),
		3: MathList._gen_len_attr(*tuple('xyz')),
		4: MathList._gen_len_attr(*tuple('wxyz')),
	}

class UserPoint(UserObj, AbstractPoint, Final):

	_parse_args_regex = r'^(?P<name>\w+)\s*=\s*(?:point|UserPoint|p|\w+)\s*[(].*[)]\s*$'

	def __init__(self, *args, **kwargs):
		super().__init__(list_args = args, **kwargs)