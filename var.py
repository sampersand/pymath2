from typing import Any
from pymath2 import Undefined
from pymath2.objs import named_valued_obj, operable
class var(named_valued_obj, operable):
	def __init__(self, name: str = Undefined, value: Any = Undefined) -> None:
		super().__init__(name = name, value = value)
		