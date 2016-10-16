from typing import Callable
from pymath2 import Undefined
from pymath2.builtins.objs.named_obj import NamedObj
from .seeded_function import SeededFunction
class UnseededFunction(NamedObj):
	seeded_type = SeededFunction
	# def __init__(self,
	# 			 inp_func: Callable,
	# 			 name: str = Undefined,
	# 			 args_str: str = Undefined,
	# 			 body_str: str = Undefined,
	# 	) -> None:
	def __init__(self, wrapped_function: Callable, name: str = Undefined,
				 args_str: str = Undefined, body_str: str = Undefined,) -> None:
		super().__init__(name)
		self.wrapped_function = wrapped_function
		if isinstance(args_str, (list, tuple)):
			args_str = ', '.join(str(x) for x in args_str)
		self.args_str = args_str
		self.body_str = body_str
	@property
	def req_arg_len(self) -> int:
		return self.wrapped_function.__code__.co_argcount

	def __call__(self, *args_str: tuple) -> seeded_type:
		if __debug__:
			assert len(args_str) == self.req_arg_len, 'length mismatch'
		return self.seeded_type(self, tuple(self.scrub(arg) for arg in args_str))

	@staticmethod
	def _gen_unseeded_str(name, args_str, body_str):
		return '{}({}) = {}'.format(name, args_str, body_str)

	def __str__(self) -> str:
		return self._gen_unseeded_str(self.name, self.args_str, self.body_str)

	def __repr__(self) -> str:
		return '{}({!r}{})'.format(type(self).__qualname__, self.wrapped_function,
									repr(self.name) if self.hasname else '')
		