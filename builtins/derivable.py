from pymath2 import Undefined
from .objs.math_obj import MathObj

class Derivable(MathObj):

	def isconst(self, du: 'Variable') -> bool:
		raise NotImplementedError

	def deriv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		return Undefined

	def d(self, other: 'Variable') -> 'UnseededFunction':
		from .derivative import Derivative
		return Derivative(self) / Derivative(other)
