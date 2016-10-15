from typing import Callable
from pymath2 import Undefined
from pymath2.functions import SeededFunction
from pymath2.objs import NamedObj
class UnseededFunction(NamedObj):
	def __init__(self,
				 inp_func: Callable,
				 name: str = Undefined,
				 args_str: str = Undefined,
				 body_str: str = Undefined,
		) -> None:
		super().__init__(name)
		self._func = inp_func
		self.args_str = args_str
		self.body_str = body_str

	@property
	def arg_len(self) -> int:
		return self._func.__code__.co_argcount

	def __call__(self, *args) -> SeededFunction:
		if __debug__:
			assert len(args) == self.arg_len, 'length mismatch'
		return SeededFunction(self, args)

	def __str__(self) -> str:
		return '{}({}) = {}'.format(self.name, self.args_str, self.body_str)

	def __repr__(self) -> str:
		return '{}({!r}{})'.format(type(self).__qualname__, self._func,
									repr(self.name) if self.hasname else '')
		