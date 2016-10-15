from typing import Any
from pymath2 import Undefined
from pymath2.objs import NamedValuedObj, Operable
class Variable(NamedValuedObj, Operable):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		super().__init__(name = name, value = value)
		