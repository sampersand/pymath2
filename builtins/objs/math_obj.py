from inspect import stack
from typing import Any
from pymath2 import Undefined, complete, final, iscoroutine
class foo():
	def __init__(self, a):
		self._a = a
	def __call__(self, there, *args, **kwargs):
			# cb = self._a._maybe_complete_func(*args, **kwargs)
			# quit('cb:'+str(cb))
			# return callback(self._a._maybe_complete_func(*args, **kwargs))
		# try:
		c = self._a.__acall__(*args, **kwargs)
		# c = complete(*args, **kwargs)
		# except AssertionError:
			# c = Undefined
		# finally:
		there.send(complete(c))

		# quit('no')
		# return complete(*args)
the_thing_to_complete = None
def bar(there):
	global the_thing_to_complete
	print('the_thing_to_complete in bar:', the_thing_to_complete)
	there.send(complete(the_thing_to_complete))
class MathObj():

	@final
	@classmethod
	def _complete_class_func(cls, *args, **kwargs):
		async_name = cls._get_async_name(stack()[1][3])
		assert hasattr(cls, async_name)
		ret = getattr(cls, async_name)(cls, *args, **kwargs)
		ret = complete(ret)
		return ret

	@final
	def _complete_func(self, *args, **kwargs):
		return self._maybe_complete_func(*args, docomp = True, stack_pos = 2, **kwargs)
		# async_name = self._get_async_name(stack()[1][3])
		# assert hasattr(self, async_name)
		# ret = getattr(self, async_name)(*args, **kwargs)
		# ret = complete(ret)
		# return ret

	@final
	def _maybe_complete_func(self, *args, docomp = None,
					async_name = None, stack_pos = 1, callback = None, **kwargs):
		async_name = async_name or self._get_async_name(stack()[stack_pos][3])
		assert hasattr(self, async_name)
		coro = getattr(self, async_name)(*args, **kwargs)
		# docomp = True
		if docomp == None or docomp:
				# from multiprocessing import Pipe, Process
				# here, there = Pipe()
				# global the_thing_to_complete
				# the_thing_to_complete = coro
				# print('the_thing_to_complete in _maybe_complete_func:', the_thing_to_complete)
				# t = Process(target = bar, args = (there, ))
				# t.start()
				# to_return = here.recv()
				# t.join()
				to_return = complete(coro)
		return to_return


	@final
	def __new__(cls, *args, **kwargs):
		return cls._complete_class_func(*args, **kwargs)

	async def __anew__(cls, *args, **kwargs):
		new = super().__new__(cls)
		# print(cls)
		await new.__ainit__(*args, **kwargs)
		super(MathObj, new).__init__()
		return new

	def __init__(self, *args, **kwargs):
		return self._complete_func(*args, **kwargs)

	async def __ainit__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@staticmethod
	def _get_async_name(name):
		if name[:2] == '__':
			return '{}a{}'.format(name[:2], name[2:])
		if name[:1] == '_':
			return '{}a{}'.format(name[:1], name[1:])
		return None

	@staticmethod
	async def async_getattr(obj, attr: str = '__repr__'):
		async_name = MathObj._get_async_name(attr)
		if async_name != None and hasattr(obj, async_name):
			return await getattr(obj, async_name)()
		return getattr(obj, attr)

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	@final
	def __str__(self) -> str: return self._complete_func()
	async def __astr__(self) -> str: return self.generic_str('default')

	@final
	def __repr__(self) -> str: return self._complete_func()
	async def __arepr__(self) -> str: return '{}()'.format(self.__class__.__name__)

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
	def __ne__(self, other: Any) -> bool: return self._complete_func(other)
	async def __ane__(self, other: Any) -> bool: return not await self.__aeq__(other)

	@final
	def __eq__(self, other: Any) -> bool: return self._complete_func(other)
	async def __aeq__(self, other: Any) -> bool: return super().__eq__(other)

	@final
	def __call__(self, *args, **kwargs):
		# from multiprocessing import Pipe, Process
		# import threading
		# here, there = Pipe()
		# pr = Process(target = foo(self), args = (there, *args), kwargs = kwargs)
		# pr.start()
		# ret = here.recv()
		# pr.join()
		# with multiprocessing.Pool() as p:
		# 	# f = lambda: self._maybe_complete_func
		# 	a = p.apply_async(foo(), (args, kwargs))
		# 	ret = a.get(timeout = .01)
		# ret = self._maybe_complete_func(*args, **kwargs)
		# assert 0
		return self._complete_func(*args, **kwargs)
		# return ret
	async def __acall__(self, *args, **kwargs): raise NotImplementedError

	# @final
	# def __getattr__(self, attr): return self._complete_func(attr)
	# async def __agetattr__(self, attr): return super().__getattr__(attr)

	# @final
	# def __setattr__(self, name, val):
	# 	#argh i gotta fix this later
	# 	assert False, "don't use non-async functions!"
	# 	return complete(self.__asetattr__(name, val))
	async def __asetattr__(self, name, val):
		return super().__setattr__(name, val)

	@final
	def __delattr__(self, name): return self._complete_func(name)
	async def __adelattr__(self, name):
		return super().__delattr__(name, val)


	async def _ahasattr(self, attr_or_obj, attr = None):
		try: 
			if attr == None:
				await getattr(self, attr_or_obj)
			else:
				await getattr(attr_or_obj, attr)
			return True
		except AttributeError:
			return False
		
	# def __hash__(self):
	# 	ret = []
	# 	for key, value in self.__dict__.items():
	# 		if not hasattr(key, '__hash__'):
	# 			key = 0
	# 		if not hasattr(value, '__hash__'):

	# 	return hash(sum(hash(key) + hash(value) for key, value in self.__dict__.items()))
















