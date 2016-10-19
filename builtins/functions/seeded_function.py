from typing import Any
from pymath2 import Undefined
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
	def value(self) -> Any:
		if self.args == Undefined:
			return Undefined
		wrap_func = self.unseeded_base_object.wrapped_function
		wrap_func = wrap_func #await
		called = wrap_func(*self.args)
		# called = called #await
		scrubbed = self.scrub(called)
		return scrubbed
		return self.scrub(self.unseeded_base_object.wrapped_function(*self.args)) #double await

	@property
	def hasvalue(self) -> Any:
		return (self.value).hasvalue #double await

	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		return '{}{}({})'.format(self.name,
								 self.unseeded_base_object._prime_str(self.unseeded_base_object.deriv_num),
								 str(self.args) if self.args is Undefined else ', '.join(str(x) for x in self.args))

	def __repr__(self) -> str:
		return '{}({!r}{}{})'.format(type(self).__qualname__, self.unseeded_base_object, 
			', {!r}'.format(self.args) if self.args is not Undefined else '',
			', {!r}'.format(self.args) if self.name is not Undefined else '',)

	def isconst(self, du):
		return self.hasvalue #await #maybe something with du? 


	# def deriv(self, du: Variable) -> 'SeededFunction':
	# 	derviative = (self.value).deriv(du)
	# 	print(derviative)
	# 	quit()


	@staticmethod
	def _gen_wrapped_func(val, du):
		deriv = val.deriv(du)
		# print(deriv)
		# b = deriv.unseeded_base_object.wrapped_function
		# print(b)
		# quit()
		# def y(): pass
		# import types
		# yc = y.__code__
		# y_code = types.CodeType(deriv.unseeded_base_object.req_arg_len, 0,
		#             yc.co_nlocals,
		#             yc.co_stacksize,
		#             yc.co_flags,
		#             yc.co_code,
		#             yc.co_consts,
		#             yc.co_names,
		#             yc.co_varnames,
		#             yc.co_filename,
		#             'f',
		#             yc.co_firstlineno,
		#             yc.co_lnotab)
		# print('I\'m here')

		# return types.FunctionType(y_code, y.__globals__, 'f')
		return lambda *args: deriv

	def deriv(self, du: Variable) -> 'UnseededFunction':
		from .unseeded_function import UnseededFunction

		req_arg_len = self.unseeded_base_object.req_arg_len #future
		wrapd_func = self._gen_wrapped_func(self.value, du)
		uns_func =  UnseededFunction(wrapd_func, #await
						      name = self.name,
						      deriv_num = self.unseeded_base_object.deriv_num + 1,
						      req_arg_len = req_arg_len, #await
						      args_str = self.unseeded_base_object.args_str,
						      body_str = str(wrapd_func))
		return uns_func
		# print(derived_function)
	def deriv(self, du: Variable) -> 'SeededFunction':
		return self.value.deriv(du)




