from pymath2 import Undefined
from pymath2.exceptions.unknown_type_error import UnknownTypeError
class MathObj():
	def __init__(self) -> None:
		pass

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	def __str__(self) -> str:
		return self.generic_str('default')

	def __repr__(self) -> str:
		return '{}()'.format(type(self).__qualname__)

	@staticmethod
	def scrub(arg):
		if isinstance(arg, MathObj) or arg is Undefined:
			return arg
		elif isinstance(arg, (int, float, bool, complex)):
			from pymath2.constant import Constant
			return Constant(arg)
		else:
			raise UnknownTypeError(type(arg))
