from typing import Any
from pymath2 import Undefined
from pymath2.builtins.objs.valued_obj import ValuedObj
from pymath2.builtins.objs.operable import Operable

class Constant(ValuedObj, Operable):
	def __init__(self, value: Any = Undefined) -> None:
		ValuedObj.__init__(self, value = value)

	async def deriv(self, du) -> 0:
		return 0