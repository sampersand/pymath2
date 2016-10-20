from pymath2 import Undefined, Constant, Final
from .math_list import MathList
from pymath2.builtins.objs.user_obj import UserObj
class AbstractVector(MathList):
	print_parens = ('<', '>')

	_len_attrs = {
		2: MathList._gen_len_attr('xy', 'ij'),
		3: MathList._gen_len_attr('xyz', 'ijk'),
		4: MathList._gen_len_attr('wxyz'),
	}


	@property
	def unit(self):
		self_val = abs(self)
		return type(self)(*(x / self_val for x in self), name = Undefined)

	@staticmethod
	def from_points(p1, p2):
		if p1.name is Undefined or p2.name is Undefined:
			name = Undefined
		else:
			name = '{}{}_'.format(p1.name, p2.name)
		return type(self)(*(x[1] - x[0] for x in zip(p1, p2)), name = name)

	def deriv(self, du):
		return type(self)(*(arg.deriv(du) for arg in self))

	def dot(self, other):
		return sum(x[0] * x[1] for x in zip(self, other))

	def __mul__(self, other):
		other = self.scrub(other)
		if hasattr(other, 'hasvalue') and other.hasvalue:
			return type(self)(*(d * other for d in self))

	def __abs__(self):
		return abs(sum(x.value ** 2 for x in self) ** .5)


@Final()
class UserVector(UserObj, AbstractVector):
	_parse_args_regex = r'^(?P<name>\w+)\s*=\s*(?:vector|UserVector|v|\w+)\s*[(].*[)]\s*$'

	def __init__(self, *args):
		super().__init__(list_args = args)



























