from typing import Any
from pymath2 import Undefined
from pymath2.objs import valued_obj, operable
class const(valued_obj, operable):
	def __init__(self, value: Any = Undefined) -> None:
		super().__init__(value = value)