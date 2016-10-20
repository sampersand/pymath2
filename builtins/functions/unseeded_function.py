from typing import Callable
from pymath2 import Undefined, Override, Final
from pymath2.builtins.objs.named_obj import NamedObj
from pymath2.builtins.objs.user_obj import UserObj
from .seeded_function import SeededFunction
class UnseededFunction(NamedObj):
	seeded_type = SeededFunction

	@Override(NamedObj)
	def __init__(self,
				 func: Callable = Undefined,
				 args_str: str = Undefined,
				 body_str: str = Undefined,
				 req_arg_len = Undefined,
				 deriv_num = 0,
				 **kwargs) -> None:
		super().__init__(**kwargs)
		self.func = func
		if isinstance(args_str, (list, tuple)):
			args_str = ', '.join(str(x) for x in args_str)
		self.args_str = args_str
		self.body_str = body_str
		self._req_arg_len = req_arg_len
		self.deriv_num = deriv_num

	@property
	def func(self) -> Callable:
		return self._func

	@func.setter
	def func(self, val: Callable) -> None:
		self._func = val

	@staticmethod
	def _prime_str(deriv_num):
		if deriv_num > 3:
			return '^{}'.format(deriv_num)
		return "'" * deriv_num

	@property
	def req_arg_len(self) -> int:
		return self._req_arg_len if self._req_arg_len is not Undefined else (self.func).__code__.co_argcount #await

	def __call__(self, *args: tuple) -> seeded_type:
		if __debug__:
			assert len(args) == self.req_arg_len or self.req_arg_len == -1, 'length mismatch between {} and {}'.format(len(args), self.req_arg_len)
		return self.seeded_type(unseeded_base_object = self, args = tuple(self.scrub(arg) for arg in args))

	@staticmethod
	def _gen_unseeded_str(name, deriv_num, args_str, body_str):
		return '{}{}({}) = {}'.format(name, UnseededFunction._prime_str(deriv_num), args_str, body_str)

	@Override(NamedObj)
	def __str__(self) -> str:
		return self._gen_unseeded_str(self.name, self.deriv_num, self.args_str, self.body_str)

	@Override(NamedObj)
	def __repr__(self) -> str:
		return '{}({!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
				self.__class__.__qualname__,
				self.func,
				self.name,
				self.args_str,
				self.body_str,
				self.req_arg_len,
				self.deriv_num)


@Final()
class UserFunction(UserObj, UnseededFunction):
	_parse_args_regex = r'''(?x)^
		(?P<name>\w+)\s*=\s*
		(?:func|UserFunction|\w+)[(]
			lambda\s+
				(?P<args_str>
					(?:\w+\s*,?\s*)*
				)
			\s*:\s*(?P<body_str>.*)
			(?:\s*,\s*deriv_num\s*=\s*
				(?P<deriv_num>\d+)
			)?\s*[)]\s*$
	'''

	@Override(UserObj)
	@staticmethod
	def process_match(match):
		match['req_arg_len'] = match['args_str'].count(',') + 1
		if match['deriv_num'] == None:
			match['deriv_num'] = 0
		if __debug__:
			assert all(x in match for x in ('name', 'args_str', 'body_str', 'req_arg_len', 'deriv_num')), match
		return match







