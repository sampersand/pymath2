from typing import Callable
from pymath2 import Undefined
from pymath2.objs.named_obj import NamedObj
from .seeded_function import SeededFunction
class UnseededFunction(NamedObj):
	seeded_type = SeededFunction
	# def __init__(self,
	# 			 inp_func: Callable,
	# 			 name: str = Undefined,
	# 			 args_str: str = Undefined,
	# 			 body_str: str = Undefined,
	# 	) -> None:
	def __init__(self,
				 wrapped_function: Callable,
				 name: str = Undefined,
				 args: str = Undefined,
				 body: str = Undefined,
		) -> None:
		super().__init__(name)
		self.wrapped_function = wrapped_function
		self.args_str = args
		self.body_str = body
	@property
	def req_arg_len(self) -> int:
		return self.wrapped_function.__code__.co_argcount

	def __call__(self, *args) -> seeded_type:
		if __debug__:
			assert len(args) == self.req_arg_len, 'length mismatch'
		return self.seeded_type(self, tuple(self.scrub(arg) for arg in args))

	def __str__(self) -> str:
		return '{}({}) = {}'.format(self.name, ', '.join(str(x) for x in self.args_str),
			self.body_str)

	def __repr__(self) -> str:
		return '{}({!r}{})'.format(type(self).__qualname__, self.wrapped_function,
									repr(self.name) if self.hasname else '')
		