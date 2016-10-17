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
		return asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(n.deriv(d)))
	def __init__(self, n: 'Derivative', d: 'Derivative') -> None:
		super().__init__(self._gen_derivative(n.value, d.value),
				name = '{}/{}'.format(n.name, d.name),
				args = (d.value, ))
		self.n = n
		self.d = d

	def __call__(self, *args):
		self.args = args
		return self

	def __str__(self) -> str:
		return str(self.value if self.hasvalue else self.name)

class Derivative(NamedValuedObj):
	def __init__(self, value: NamedValuedObj) -> None:
		super().__init__(name = 'd{}'.format(value.name), value = value)

	def __truediv__(self, other: 'Derivative') -> SeededDerivative:
		if not isinstance(other, Derivative):
			return NotImplemented
		return SeededDerivative(self, other)

	def __str__(self) -> str:
		return self.name