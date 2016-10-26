import asyncio
from typing import Callable


from . import logger

from pymath2 import Undefined, override, final, complete, ensure_future, finish

from pymath2.builtins.objs.named_obj import NamedObj
from pymath2.builtins.objs.user_obj import UserObj

from .seeded_function import SeededFunction
from .seeded_operator import SeededOperator

from pymath2.builtins.variable import Variable
from pymath2.builtins.constant import Constant


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
		ainit = ensure_future(super().__ainit__(**kwargs))
		afunc = ensure_future(self._afunc_setter(func))

		if isinstance(args_str, (list, tuple)):
			args_str = ', '.join(str(x) for x in args_str)

		aargs = ensure_future(self.__asetattr__('args_str', args_str))
		abody = ensure_future(self.__asetattr__('body_str', body_str))
		areql = ensure_future(self.__asetattr__('_req_arg_len', req_arg_len))
		adnum = ensure_future(self.__asetattr__('deriv_num', deriv_num))
		await ainit; await afunc; await aargs
		await abody; await areql; await adnum

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
		await self.__asetattr__('_func', val)

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
		fut_args = [ensure_future(self.scrub(arg)) for arg in args]
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
		name = await self.get_asyncattr(await self._aname, '__str__')
		return await self._gen_unseeded_str(name, self.deriv_num, self.args_str, self.body_str)

	@override(NamedObj)
	async def __arepr__(self) -> str:
		func = ensure_future(self._afunc)
		name = ensure_future(self._aname)
		return '{}({!r}, {}, {}, {!r}, {!r}, {!r})'.format(
				self.__class__.__qualname__,
				self.get_asyncattr(await func),
				self.get_asyncattr(await name),
				self.args_str,
				self.body_str,
				self.req_arg_len,
				self.deriv_num)

@final
class UserFunction(UserObj, UnseededFunction):
	_parse_args_regex = r'''(?x)^
		\s*(?P<name>\w+)\s*=\s*
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

	async def __ainit__(self, lambda_object, arg_count = Undefined, **kwargs):
		arg_count = lambda_object.__code__.co_argcount if arg_count is Undefined else arg_count

		# async with finish():
		# 	vars_ = [future(Variable.__anew__(Variable)) for x in range(arg_count)]
		vars_ = []
		for x in range(arg_count):
			vars_.append(await Variable.__anew__(Variable))
		# vars_ = [x.result() for x in vars_]
		
		old_event_loop = asyncio.get_event_loop()
		asyncio.set_event_loop(asyncio.new_event_loop())

		if not callable(lambda_object):
			raise ValueError('lambda_object needs to be callable!')
		self.lambda_result = await self.scrub(lambda_object(*vars_))
		asyncio.set_event_loop(old_event_loop)

		await super().__ainit__(**kwargs)

	# def __call__(self, *args, **kwargs):
	# 	quit()
	@override(UnseededFunction)
	@property
	async def _afunc(self) -> Callable:
		if isinstance(self.lambda_result, (Variable, Constant)):
			print('isvar')
			return lambda x: x
		if type(self.lambda_result) == SeededOperator:
			lr = await self.lambda_result.copy()
			def foo(*args):
				lr._new_result_replace(args)
				assert lr is not None
				return lr
			return foo
		if type(self.lambda_result) == SeededFunction:
			# lr = await self.lambda_result.copy()
			lrf = await self.lambda_result.unseeded_base_object._afunc
			def foo(*args):
				lr = lrf(*args)
				lr._new_result_replace(args)
				assert lr is not None
				return lr
			return foo
		quit('nope dont go there')
		# lr = await self.lambda_result.copy()
		# print(type(lr), type(self.lambda_result))
		# def foo(*args):
		# 	lr._new_result_replace(args)
		# 	return lr
		# return foo
		# return self.lambda_result


	@override(UserObj)
	@staticmethod
	def process_match(match):
		match['req_arg_len'] = match['args_str'].count(',') + 1
		if match['deriv_num'] == None:
			match['deriv_num'] = 0

		assert all(x in match for x in ('name', 'args_str', 'body_str', 'req_arg_len', 'deriv_num')), match

		return match






