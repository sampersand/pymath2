from typing import Callable
from pymath2 import Undefined, await_result
from pymath2.builtins.objs.named_obj import NamedObj
from .seeded_function import SeededFunction
class UnseededFunction(NamedObj):
	seeded_type = SeededFunction
	def __init__(self, wrapped_function: Callable = Undefined, name: str = Undefined,
				 args_str: str = Undefined, body_str: str = Undefined,
				 req_arg_len = Undefined, deriv_num = 0) -> None:
		super().__init__(name)
		self._wrapped_function = wrapped_function
		if isinstance(args_str, (list, tuple)):
			args_str = ', '.join(str(x) for x in args_str)
		self.args_str = args_str
		self.body_str = body_str
		self._req_arg_len = req_arg_len
		self.deriv_num = deriv_num

	def wrapped_function():
		async def fget(self) -> Callable:
			return self._wrapped_function
		def fset(self, val: Callable) -> None:
			self._wrapped_function = val
		return locals()
	wrapped_function = property(**wrapped_function())

	@property
	def _prime_str(self):
		if self.deriv_num > 3:
			return '^{}'.format(self.deriv_num)
		return "'" * self.deriv_num

	@property
	async def req_arg_len(self) -> int:
		return self._req_arg_len if self._req_arg_len is not Undefined else (await self.wrapped_function).__code__.co_argcount

	def __call__(self, *args_str: tuple) -> seeded_type:
		if __debug__:
			assert len(args_str) == await_result(self.req_arg_len) or await_result(self.req_arg_len) == -1,\
				'length mismatch between {} and {}'.format(len(args_str), await_result(self.req_arg_len))
		return self.seeded_type(self, tuple(self.scrub(arg) for arg in args_str))

	@staticmethod
	def _gen_unseeded_str(name, args_str, body_str):
		return '{}({}) = {}'.format(name, args_str, body_str)

	def __str__(self) -> str:
		return self._gen_unseeded_str(self.name, self.args_str, self.body_str)

	def __repr__(self) -> str:
		return '{}({!r}{})'.format(type(self).__qualname__, await_result(self.wrapped_function),
									repr(self.name) if self.hasname else '')
		