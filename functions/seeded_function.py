from typing import Any
from pymath2.objs.named_valued_obj import NamedValuedObj
from pymath2.objs.operable import Operable
class SeededFunction(NamedValuedObj, Operable):
	def __init__(self, unseeded_instance: 'UnSeededFunction', args: tuple) -> None:
		super().__init__()
		self.testie = unseeded_instance
		self.args = args

	@property
	def value(self) -> Any:
		return self.scrub(self.testie.callable_func(*self.args))

	@property
	def hasvalue(self) -> any:
		return self.value.hasvalue

	@property
	def name(self) -> str:
		return self.testie.name

	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		return '{}({})'.format(self.name, ', '.join(str(x) for x in self.args))

