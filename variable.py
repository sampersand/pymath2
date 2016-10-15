from typing import Any
from pymath2 import Undefined
from pymath2.objs.named_valued_obj import NamedValuedObj
from pymath2.objs.operable import Operable
class Variable(NamedValuedObj, Operable):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		super().__init__(name = name, value = value)
		