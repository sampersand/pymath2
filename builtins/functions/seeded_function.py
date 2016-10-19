from typing import Any
from pymath2 import Undefined, await_result, future
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.operable import Operable
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
class SeededFunction(NamedValuedObj, Operable):
	def __init__(self, unseeded_instance: 'UnseededFunction', args: tuple = Undefined, name: str = Undefined) -> None:
		super().__init__(name = name)
		if __debug__:
			from .unseeded_function import UnseededFunction
			assert isinstance(unseeded_instance, UnseededFunction), '{}, type {}'.format(unseeded_instance, type(unseeded_instance))
		self.unseeded_base_object = unseeded_instance
		self.args = args

	@property
	def name(self):
		return self._name if self._name is not Undefined else self.unseeded_base_object.name

	@property
	async def value(self) -> Any:
		if self.args == Undefined:
			return Undefined
		wrap_func = self.unseeded_base_object.wrapped_function
		wrap_func = await wrap_func
		called = wrap_func(*self.args)
		# called = await called
		scrubbed = self.scrub(called)
		return scrubbed
		return self.scrub(await (await self.unseeded_base_object.wrapped_function)(*self.args))

	@property
	async def hasvalue(self) -> Any:
		return await (await self.value).hasvalue

	def __str__(self) -> str:
		if await_result(self.hasvalue):
			return str(await_result(self.value))
		return '{}{}({})'.format(self.name,
								 self.unseeded_base_object._prime_str,
								 str(self.args) if self.args is Undefined else ', '.join(str(x) for x in self.args))

	def __repr__(self) -> str:
		return '{}({!r}{}{})'.format(type(self).__qualname__, self.unseeded_base_object, 
			', {!r}'.format(self.args) if self.args is not Undefined else '',
			', {!r}'.format(self.args) if self.name is not Undefined else '',)

	async def isconst(self, du):
		return await self.hasvalue #maybe something with du?


	async def _get_derived_function(self, du):
		# print('boilerplate func: _get_derived_function')
		deriv = await (await self.value).deriv(du)
		def y(): pass
		# import types
		# y_code = types.CodeType(deriv.unseeded_base_object.req_arg_len, 0,
		#             y.__code__.co_nlocals,
		#             y.__code__.co_stacksize,
		#             y.__code__.co_flags,
		#             y.__code__.co_code,
		#             y.__code__.co_consts,
		#             y.__code__.co_names,
		#             y.__code__.co_varnames,
		#             y.__code__.co_filename,
		#             'f',
		#             y.__code__.co_firstlineno,
		#             y.__code__.co_lnotab)
		print('I\'m here')

		# return types.FunctionType(y_code, y.__globals__, 'f')
		return lambda *args: deriv

	async def deriv(self, du: Variable) -> 'UnseededFunction':
		from .unseeded_function import UnseededFunction
		# assert 0
		wrapd_func = future(self._get_derived_function(du))
		req_arg_len = future(self.unseeded_base_object.req_arg_len)
		uns_func =  UnseededFunction(await wrapd_func, 
						      name = self.name,
						      deriv_num = self.unseeded_base_object.deriv_num + 1,
						      req_arg_len = await req_arg_len, 
						      args_str = self.unseeded_base_object.args_str)
		# print(wrapd_func, uns_func)
		# print(uns_func.req_arg_len)
		seed_func = uns_func(*self.args)
		return seed_func
		# print(derived_function)





