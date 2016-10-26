from pymath2 import Undefined, final, override
from .math_list import MathList
from pymath2.builtins.objs.user_obj import UserObj
class AbstractPoint(MathList):
	print_parens = ('(', ')')

	_len_attrs = {
		2: MathList._gen_len_attr(*tuple('xy')),
		3: MathList._gen_len_attr(*tuple('xyz')),
		4: MathList._gen_len_attr(*tuple('wxyz')),
	}

@final
class UserPoint(UserObj, AbstractPoint):

	_parse_args_regex = r'^(?P<name>\w+)\s*=\s*(?:point|UserPoint|p|\w+)\s*[(].*[)]\s*$'
	override(UserObj, name = '_parse_args_regex')

	async def __ainit__(self, *args, **kwargs):
		assert inloop()
		super().__ainit__(list_args = args, **kwargs)