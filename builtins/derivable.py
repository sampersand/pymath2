from typing import TYPE_CHECKING
from pymath2 import final, complete
from .objs.math_obj import MathObj

from pymath2 import Undefined, complete, inloop

class Derivable(MathObj):


	@final
	def isconst(self, du: 'Variable') -> bool:
		assert not inloop()
		return complete(self._aisconst(du))

	async def _aisconst(self, du: 'Variable') -> bool:
		assert inloop()
		raise NotImplementedError

	@final
	def deriv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		assert not inloop()
		if __debug__:
			from .variable import Variable
		assert isinstance(du, Variable), 'Can only take derivative with regards to Variable, not {}'.format(type(du))
		return complete(self._aderiv(du))

	async def _aderiv(self, du: 'Variable') -> ('ValuedObj', Undefined):
		assert inloop()
		raise NotImplementedError

	@final
	def d(self, du: 'Variable') -> 'UnseededFunction':
		assert not inloop()
		if __debug__:
			from .variable import Variable
		assert isinstance(du, Variable), 'Can only take derivative with regards to Variable, not {}'.format(type(du))
		from .derivative import Derivative
		return complete(Derivative._a_get_deriv(self, du))
	


