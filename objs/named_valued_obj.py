from typing import Any
from pymath2 import Undefined
from pymath2.objs.named_obj import named_obj
from pymath2.objs.valued_obj import valued_obj

class named_valued_obj(named_obj, valued_obj):
	def __init__(self, name: str = Undefined, value: Any = Undefined):
		named_obj.__init__(self, name)
		valued_obj.__init__(self, value)

	def __str__(self) -> str:
		return valued_obj.__str__(self) if self.hasvalue else named_obj.__str__(self)

	def __repr__(self) -> str:
		return '{}({!r}, {!r})'.format(type(self).__qualname__,
					self.name,
					self.value)

