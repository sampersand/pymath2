from typing import Any
from pymath2 import Undefined
class MathObj():

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	def __str__(self) -> str:
		return self.generic_str('default')

	def __repr__(self) -> str:
		return '{}()'.format(self.__class__.__name__)

	@staticmethod
	def scrub(arg: Any) -> 'MathObj':
		if isinstance(arg, MathObj) or arg is Undefined:
			return arg
		elif isinstance(arg, (int, float, bool, complex)):
			from pymath2.builtins.constant import Constant
			return Constant(arg)
		elif isinstance(arg, (tuple, list)):
			from pymath2.extensions.math_list import MathList
			return MathList(*arg)
		elif arg == None:
			return Undefined
		else:
			raise TypeError(type(arg))

	def __ne__(self, other: Any) -> bool:
		return not(self == other)