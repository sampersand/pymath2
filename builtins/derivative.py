import asyncio
from typing import Any
from pymath2 import Undefined, future
from .objs.math_obj import MathObj
from .functions.unseeded_function import UnseededFunction
from .functions.seeded_function import SeededFunction
from .objs.valued_obj import ValuedObj
from .objs.named_valued_obj import NamedValuedObj
# class SeededDerivative(SeededFunction):
# 	@staticmethod
# 	def _gen_derivative(n, d):
# 		nd = n.deriv(d)
# 		ndfuture = asyncio.ensure_future(nd)
# 		print(ndfuture)
# 		res = asyncio.get_event_loop().run_until_complete(ndfuture)
# 		print(res)
# 		# quit()
# 		return res
# 		# return asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(n.deriv(d))) 
# 	def __init__(self, n: 'Derivative', d: 'Derivative') -> None:
# 		super().__init__(self._gen_derivative(n.value, d.value),
# 				name = '{}/{}'.format(n.name, d.name), args = (d.value,))
# 		self.n = n
# 		self.d = d

# 	def __call__(self, *args):
# 		self.args = args
# 		return self

# 	def __str__(self) -> str:
# 		return str(self.value if self.hasvalue else self.name)

class Derivative(NamedValuedObj):

	def __init__(self, value: NamedValuedObj) -> None:
		super().__init__(name = 'd{}'.format(value.name), value = value)
		# print(type(value), isinstance(value, SeededFunction))
	def __truediv__(self, other: 'Derivative') -> 'SeededDerivative':
		if not isinstance(other, Derivative):
			return NotImplemented
		return self._gen_derivative(other)

	def _gen_derivative(self, other):
		print('todo: make _gen_derivative async')
		sv = future(self.value)
		ov = future(other.value)
		# ndfuture = future((await sv).deriv(await ov))
		ndfuture = await_result(sv).deriv(await_result(ov))
		return await_result(ndfuture)

	def __str__(self) -> str:
		return self.name








