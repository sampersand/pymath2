from pymath2 import Undefined
from . import obj
class named_obj(obj):
	def __init__(self, name: str = Undefined) -> None:
		super().__init__()
		self._name = name


	def name() -> dict:
		def fget(self) -> (str, Undefined):
			return self._name
			# return self._name if self.hasname else super().__str__(prefix = 'unnamed')
		def fset(self, val: str) -> None:
			self._name = val
		return locals()
	name = property(**name())

	@property
	def hasname(self) -> bool:
		return self.name is not Undefined

	def __str__(self) -> str:
		#assume self.name is a string, even though no checks
		return self.name if self.hasname else self.generic_str(prefix = 'unnamed')

	def __repr__(self) -> str:
		return '{}({!r})'.format(type(self).__qualname__, self.name)