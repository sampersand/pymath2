from typing import Any
from pymath2 import Undefined
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.operable import Operable
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
class SeededFunction(NamedValuedObj, Operable):
	def __init__(self, unseeded_instance: 'UnseededFunction', args: tuple = Undefined, name: str = Undefined) -> None:
		super().__init__(name = name)
		self.unseeded_base_object = unseeded_instance
		self.args = args

	@property
	def name(self):
		return self._name if self._name is not Undefined else self.unseeded_base_object.name

	@property
	def value(self) -> Any:
		if self.args == Undefined:
			return Undefined
		return self.scrub(self.unseeded_base_object.wrapped_function(*self.args))

	@property
	def hasvalue(self) -> Any:
		return self.value.hasvalue

	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		return '{}{}({})'.format(self.name,
								 self.unseeded_base_object._prime_str,
								 str(self.args) if self.args is Undefined else ', '.join(str(x) for x in self.args))

	def isconst(self, du):
		return self.hasvalue #maybe something with du?


	async def _get_derived_function(self, du):
		# print('boilerplate func: _get_derived_function')
		deriv = await self.value.deriv(du)
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

		# return types.FunctionType(y_code, y.__globals__, 'f')
		return lambda *args: deriv

	async def deriv(self, du: Variable) -> 'UnseededFunction':
		from .unseeded_function import UnseededFunction
		# assert 0
		return UnseededFunction(await self._get_derived_function(du), 
						      name = self.name,
						      deriv_num = self.unseeded_base_object.deriv_num + 1,
						      args_str = self.unseeded_base_object.args_str)
		# print(derived_function)





