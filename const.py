from typing import Any
from pymath2 import Undefined
from pymath2.objs.valued_obj import valued_obj
from pymath2.objs.operable import operable
class const(valued_obj, operable):
	def __init__(self, value: Any = Undefined) -> None:
		super().__init__(value = value)