from typing import Any
from pymath2 import Undefined
from pymath2.objs import ValuedObj, Operable
class Constant(ValuedObj, Operable):
	def __init__(self, value: Any = Undefined) -> None:
		super().__init__(value = value)