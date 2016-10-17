import asyncio
from pymath2 import Undefined
from .objs.math_obj import MathObj
from .functions.unseeded_function import UnseededFunction
from .functions.seeded_function import SeededFunction
from .objs.valued_obj import ValuedObj
from .objs.named_valued_obj import NamedValuedObj
class SeededDerivative(SeededFunction):
	@staticmethod
	def _gen_derivative(n, d):
		async def foo():
			val = n.deriv(d)
			print("val:",val)
			awaited_val = await val
			print('awaited_val:', awaited_val)
			return awaited_val
		return asyncio.get_event_loop().run_until_complete(foo())
	def __init__(self, n: 'Derivative', d: 'Derivative') -> None:
		super().__init__(self._gen_derivative(n.value, d.value),
				name = 'd{}/d{}'.format(n.value.name, d.value.name))
		self.n = n
		self.d = d

	def __call__(self, *args):
		self.args = args
		return self

	def __str__(self) -> str:
		return str(self.value if self.hasvalue else self.name)

class Derivative(ValuedObj):
	def __init__(self, value: NamedValuedObj) -> None:
		super().__init__(value)

	def __truediv__(self, other: 'Derivative') -> SeededDerivative:
		if not isinstance(other, Derivative):
			return NotImplemented
		return SeededDerivative(self, other)

	def __str__(self) -> str:
		return 'd{}'.format(self.value.name)