from typing import Any
from pymath2 import Undefined, override
from pymath2.builtins.variable import Variable
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.derivable import Derivable
class SeededFunction(NamedValuedObj, Derivable):
	@override(NamedValuedObj)
	def __init__(self, unseeded_base_object: 'UnseededFunction', args: tuple = Undefined, **kwargs) -> None:
		super().__init__(**kwargs)
		if __debug__:
			from .unseeded_function import UnseededFunction
			assert isinstance(unseeded_base_object, UnseededFunction), '{}, type {}'.format(unseeded_base_object, type(unseeded_base_object))
		self.unseeded_base_object = unseeded_base_object
		self.args = args

	@NamedValuedObj.name.getter
	@override(NamedValuedObj)
	def name(self):
		return self._name if self._name is not Undefined else self.unseeded_base_object.name

	@NamedValuedObj.value.getter
	@override(NamedValuedObj)
	def value(self) -> Any:
		return self.scrub(self.unseeded_base_object.func(*self.args)) #double await

	@NamedValuedObj.hasvalue.getter
	@override(NamedValuedObj)
	def hasvalue(self) -> Any:
		return self.value.hasvalue #double await

	@override(NamedValuedObj)
	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		return '{}{}({})'.format(self.name,
								 self.unseeded_base_object._prime_str(self.unseeded_base_object.deriv_num),
								 str(self.args) if self.args is Undefined else ', '.join(str(x) for x in self.args))

	@override(NamedValuedObj)
	def __repr__(self) -> str:
		return '{}({!r}{}{})'.format(self.__class__.__name__, self.unseeded_base_object, 
			', {!r}'.format(self.args) if self.args is not Undefined else '',
			', {!r}'.format(self.args) if self.name is not Undefined else '',)

	@override(Derivable)
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
		# b = deriv.unseeded_base_object.func
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
		return deriv

	@override(Derivable)
	def deriv(self, du: Variable) -> 'UnseededFunction':
		from .unseeded_function import UnseededFunction

		req_arg_len = self.unseeded_base_object.req_arg_len #future
		func = self._gen_wrapped_func(self.value, du)
		func_str = str(func)
		uns_func =  UnseededFunction(
							  func = lambda *args: func(*args), #await
						      name = self.name,
						      deriv_num = self.unseeded_base_object.deriv_num + 1,
						      req_arg_len = req_arg_len, #await
						      args_str = self.unseeded_base_object.args_str,
						      body_str = func_str)
		return uns_func
		# print(derived_function)
	@override(Derivable)
	def deriv(self, du: Variable) -> 'SeededFunction':
		return self.value.deriv(du)




