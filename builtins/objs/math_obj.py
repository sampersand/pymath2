from typing import Any
from pymath2 import Undefined, complete, final
class MathObj():
	@final
	def __new__(cls, *args, **kwargs):
		assert False, "don't use non-async functions!"
		return complete(cls.__anew__(cls, *args, **kwargs))
	async def __anew__(cls, *args, **kwargs):
		new = super().__new__(cls)
		await new.__ainit__(*args, **kwargs)
		return new

	def __init__(self, *args, **kwargs):
		assert False, "don't use non-async functions!"
		return complete(self.__ainit__(*args, **kwargs))

	async def __ainit__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@staticmethod
	async def async_getattr(obj, attr: str = '__repr__'):
		if attr[:2] == '__':
			newattr = attr[:2] + 'a' + attr[2:]
			if hasattr(obj, newattr):
				return await getattr(obj, newattr)
		elif attr[:1] == '_':
			newattr = attr[:1] + 'a' + attr[1:]
			if hasattr(obj, newattr):
				return await getattr(obj, newattr)

		if hasattr(obj, attr):
			return getattr(obj, attr)

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	@final
	def __str__(self) -> str:
		assert False, "don't use non-async functions!"
		return complete(self.__astr__())
	async def __astr__(self) -> str:
		return self.generic_str('default')

	@final
	def __repr__(self) -> str:
		assert False, "don't use non-async functions!"
		return complete(self.__arepr__())
	async def __arepr__(self) -> str:
		return '{}()'.format(self.__class__.__name__)

	@staticmethod
	async def scrub(arg: Any) -> 'MathObj':
		if isinstance(arg, MathObj) or arg is Undefined:
			return arg
		elif isinstance(arg, (int, float, bool, complex)):
			from pymath2.builtins.constant import Constant
			return await Constant.__anew__(Constant, arg)
		elif isinstance(arg, (tuple, list)):
			from pymath2.extensions.math_list import MathList
			return await MathList.__anew__(MathList, *arg)
		elif arg == None:
			return Undefined
		else:
			raise TypeError(type(arg))

	@final
	def __ne__(self, other: Any) -> bool:
		assert False, "don't use non-async functions!"
		return complete(self.__ane__(other))
	async def __ane__(self, other: Any) -> bool:
		return not self.__aeq__(other)

	@final
	def __eq__(self, other: Any) -> bool:
		assert False, "don't use non-async functions!"
		assert 0, 'make sure this isnt being used incorrectly!'
		return complete(self.__aeq__(other))
	async def __aeq__(self, other: Any) -> bool:
		return super().__eq__(other)

	@final
	def __call__(self, *args, **kwargs):
		assert False, "don't use non-async functions!"
		return complete(self.__acall__(*args, **kwargs))
	async def __acall__(self, *args, **kwargs):
		raise NotImplementedError

	@final
	def __getattr__(self, attr):
		assert False, "don't use non-async functions!"
		return complete(self.__agetattr__(attr))
	async def __agetattr__(self, attr):
		return super().__getattr__(attr)

	@final
	def __setattr__(self, name, val):
		#argh i gotta fix this later
		return super().__setattr__(name, val)
		return complete(self.__asetattr__(name, val))
	async def __asetattr__(self, name, val):
		return super().__setattr__(name, val)

	@final
	def __delattr__(self, name):
		assert False, "don't use non-async functions!"
		return complete(self.__adelattr__(name))
	async def __adelattr__(self, name):
		return super().__delattr__(name, val)









