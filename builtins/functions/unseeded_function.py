from typing import Callable
from pymath2 import Undefined, override, final, complete, future
from pymath2.builtins.objs.named_obj import NamedObj
from pymath2.builtins.objs.user_obj import UserObj
from .seeded_function import SeededFunction
class UnseededFunction(NamedObj):
	seeded_type = SeededFunction

	@override(NamedObj)
	async def __ainit__(self,
				 func: Callable = Undefined,
				 args_str: str = Undefined,
				 body_str: str = Undefined,
				 req_arg_len = Undefined,
				 deriv_num = 0,
				 **kwargs) -> None:
		await super().__ainit__(**kwargs)
		await self._afunc_setter(func)
		if isinstance(args_str, (list, tuple)):
			args_str = ', '.join(str(x) for x in args_str)
		self.args_str = args_str
		self.body_str = body_str
		self._req_arg_len = req_arg_len
		self.deriv_num = deriv_num

	@final
	def func(self):
		@final
		def fget(self):
			assert False, "don't use non-async functions!"
			return complete(self._afunc)
		@final
		def fset(self, val):
			assert False, "don't use non-async functions!"
			return complete(self._afunc_setter(val))

	@property
	async def _afunc(self) -> Callable:
		return self._func

	async def _afunc_setter(self, val) -> None:
		self._func = val

	@staticmethod
	async def _aprime_str(deriv_num):
		if deriv_num > 3:
			return '^{}'.format(deriv_num)
		return "'" * deriv_num

	@property
	def req_arg_len(self) -> int:
		return self._req_arg_len if self._req_arg_len is not Undefined else\
			 self.func.__code__.co_argcount 

	@override(NamedObj)
	async def __acall__(self, *args, **kwargs) -> seeded_type:
		assert len(args) == self.req_arg_len or self.req_arg_len == -1, 'length mismatch between {} and {}'.format(len(args), self.req_arg_len)
		fut_args = [future(self.scrub(arg)) for arg in args]
		args = []
		for arg in fut_args:
			args.append(await arg)
		ret = await self.seeded_type.__anew__(
			cls = self.seeded_type,
			unseeded_base_object = self,
			args = args)
		r = ret.unseeded_base_object
		return ret

	@staticmethod
	async def _gen_unseeded_str(name, deriv_num, args_str, body_str):
		return '{}{}({}) = {}'.format(name, await UnseededFunction._aprime_str(deriv_num), args_str, body_str)



	@override(NamedObj)
	async def __astr__(self) -> str:
		name = (await self.async_getattr(await self._aname, '__str__'))()
		return await self._gen_unseeded_str(name, self.deriv_num, self.args_str, self.body_str)

	@override(NamedObj)
	async def __arepr__(self) -> str:
		func = future(self._afunc)
		name = future(self._aname)
		return '{}({!r}, {}, {}, {!r}, {!r}, {!r})'.format(
				self.__class__.__qualname__,
				self.async_getattr(await func),
				self.async_getattr(await name),
				self.args_str,
				self.body_str,
				self.req_arg_len,
				self.deriv_num)

@final
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
	override(UserObj, name = '_parse_args_regex')

	@override(UserObj)
	@staticmethod
	def process_match(match):
		match['req_arg_len'] = match['args_str'].count(',') + 1
		if match['deriv_num'] == None:
			match['deriv_num'] = 0

		assert all(x in match for x in ('name', 'args_str', 'body_str', 'req_arg_len', 'deriv_num')), match

		return match







