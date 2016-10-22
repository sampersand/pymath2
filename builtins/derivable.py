from pymath2 import Undefined, final, complete
from .objs.math_obj import MathObj

class Derivable(MathObj):

	@final
	def isconst(self, du: 'Variable') -> bool:
		assert False, "don't use non-async functions!"
		return complete(self._aisconst(du))

	async def _aisconst(self, du: 'Variable') -> bool:
		raise NotImplementedError

	@final
	def deriv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		assert False, "don't use non-async functions!"
		return complete(self._aderiv(du))

	async def _aderiv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		raise NotImplementedError

	@final
	def d(self, other: 'Variable') -> 'UnseededFunction':
		assert False, "don't use non-async functions!"
		from .derivative import Derivative
		return Derivative(self) / Derivative(other)
	