from typing import Any 
from pymath2 import Undefined, Override
from .math_obj import MathObj

class NamedObj(MathObj):
	@Override(MathObj)
	def __init__(self, name: str = Undefined, **kwargs) -> None:
		super().__init__(**kwargs)
		self._name = name

	@property
	def name(self) -> (str, Undefined):
		return self._name

	@name.setter
	def name(self, val: str) -> None:
		self._name = val

	@property
	def hasname(self) -> bool:
		return self.name is not Undefined

	@Override(MathObj)
	def __str__(self) -> str:
		return str(self.name) if self.hasname else self.generic_str(prefix = 'unnamed')

	@Override(MathObj)
	def __repr__(self) -> str:
		return '{}({!r})'.format(self.__class__.__name__, self.name)

	def __eq__(self, other: Any) -> bool:
		if not hasattr(other, 'name'):
			return False
		if self.name == other.name and self.name is not Undefined:
			return True
		return super().__eq__(other)

