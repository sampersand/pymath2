from inspect import stack
from typing import Any
from pymath2 import Undefined, complete, final, iscoroutine
if __debug__:
	from pymath2 import inloop
class MathObj():

	# @final
	# @classmethod
	# def _complete_class_func(cls, *args, **kwargs):
	# 	async_name = cls._get_async_name(stack()[1][3])
	# 	assert hasattr(cls, async_name)
	# 	ret = getattr(cls, async_name)(cls, *args, **kwargs)
	# 	ret = complete(ret)
	# 	return ret

	# @final
	# def _complete_func(self, *args, async_name = None, **kwargs):
	# 	async_name = async_name or self._get_async_name(stack()[stack_pos][3])
	# 	assert hasattr(self, async_name)
	# 	coro = getattr(self, async_name)(*args, **kwargs)
	# 	# docomp = True
	# 	to_return = complete(coro)
	# 	return to_return


	@final
	def __new__(cls, *args, **kwargs):
		assert not inloop()
		assert isinstance(cls, type)
		return complete(cls.__anew__(cls, *args, **kwargs))

	async def __anew__(cls, *args, **kwargs):
		# check this
		assert inloop()
		assert isinstance(cls, type)
		new = super().__new__(cls)
		await new.__ainit__(*args, **kwargs)
		super(MathObj, new).__init__()
		return new

	def __init__(self, *args, **kwargs):
		assert not inloop()
		return complete(self.__ainit__(*args, **kwargs))

	async def __ainit__(self, *args, **kwargs):
		assert inloop()
		super().__init__(*args, **kwargs)

	@staticmethod
	def _get_async_name(name):
		if name[:2] == '__':
			return '{}a{}'.format(name[:2], name[2:])
		if name[:1] == '_':
			return '{}a{}'.format(name[:1], name[1:])
		return None

	@staticmethod
	async def get_asyncattr(obj, attr: str = '__repr__', call = True):
		assert inloop()
		async_name = MathObj._get_async_name(attr)
		if async_name != None and hasattr(obj, async_name):
			if not call:
				return getattr(obj, async_name)
			attr = await getattr(obj, async_name)()
		else:
			attr = getattr(obj, attr)
		if hasattr(attr, '__call__'):
			return attr()
		return attr
		quit('dont go here')
		return attr

	@staticmethod
	async def has_asyncattr(obj, attr):
		assert inloop()
		async_name = MathObj._get_async_name(attr)
		return async_name and hasattr(obj, async_name)

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	@final
	def __str__(self) -> str:
		assert not inloop()
		return complete(self.__astr__())
	async def __astr__(self) -> str:
		assert inloop()
		return self.generic_str('default')

	@final
	def __repr__(self) -> str:
		assert not inloop()
		return complete(self.__arepr__())
	async def __arepr__(self) -> str:
		assert inloop()
		return '{}()'.format(self.__class__.__name__)

	@staticmethod
	async def scrub(arg: Any) -> 'MathObj':
		assert not iscoroutine(arg)
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
		assert not inloop()
		return complete(self.__ane__(other))
	async def __ane__(self, other: Any) -> bool:
		assert inloop()
		return not await self.__aeq__(other)

	@final
	def __eq__(self, other: Any) -> bool:
		assert not inloop()
		return complete(self.__aeq__(other))
	async def __aeq__(self, other: Any) -> bool:
		assert inloop()
		return super().__eq__(other)

	@final
	def __call__(self, *args, **kwargs):
		assert not inloop()
		return complete(self.__acall__(*args, **kwargs))
	async def __acall__(self, *args, **kwargs):
		assert inloop()
		raise NotImplementedError

	# @final
	# def __getattr__(self, attr): return self._complete_func(attr)
	# async def __agetattr__(self, attr): return super().__getattr__(attr)

	# @final
	# def __setattr__(self, name, val):
	# 	#argh i gotta fix this later
	# 	assert False, "don't use non-async functions!"
	# 	return complete(self.__asetattr__(name, val))
	async def __asetattr__(self, name, val):
		assert inloop()
		return super().__setattr__(name, val)

	@final
	def __delattr__(self, name):
		assert not inloop()
		return complete(self.__adelattr__(name))
	async def __adelattr__(self, name):
		assert inloop()
		return super().__delattr__(name, val)


	async def _ahasattr(self, attr_or_obj, attr = None):
		assert inloop()
		try: 
			if attr == None:
				geta = getattr(self, attr_or_obj)
			else:
				geta = getattr(attr_or_obj, attr)
			if iscoroutine(geta):
				geta = await geta 
			return geta
		except AttributeError:
			return False
		
	# def __hash__(self):
	# 	ret = []
	# 	for key, value in self.__dict__.items():
	# 		if not hasattr(key, '__hash__'):
	# 			key = 0
	# 		if not hasattr(value, '__hash__'):

	# 	return hash(sum(hash(key) + hash(value) for key, value in self.__dict__.items()))
















