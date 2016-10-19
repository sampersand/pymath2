from typing import Any 
from pymath2 import Undefined
from .math_obj import MathObj
class NamedObj(MathObj):
	def __init__(self, name: str = Undefined) -> None:
		super().__init__()
		self._name = name

	@property
	def name(self) -> (str, Undefined):
		return self._name
	@name.setter
	def setter(self, val: str) -> None:
		self._name = val

	@property
	def hasname(self) -> bool:
		return self.name is not Undefined

	def __str__(self) -> str:
		#assume self.name is a string, even though no checks
		return self.name if self.hasname else self.generic_str(prefix = 'unnamed')

	def __repr__(self) -> str:
		return '{}({!r})'.format(type(self).__qualname__, self.name)

	def __eq__(self, other: Any) -> bool:
		if not hasattr(other, 'name'):
			return False
		return self.name == other.name and self.name is not Undefined
