from typing import Any
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.objs.operable import Operable
class SeededFunction(NamedValuedObj, Operable):
	def __init__(self, unseeded_instance: 'UnSeededFunction', args: tuple) -> None:
		super().__init__()
		self.unseeded_base_object = unseeded_instance
		self.args = args

	@property
	def value(self) -> Any:
		return self.scrub(self.unseeded_base_object.wrapped_function(*self.args))

	@property
	def hasvalue(self) -> Any:
		return self.value.hasvalue

	@property
	def name(self) -> str:
		return self.unseeded_base_object.name

	def __str__(self) -> str:
		if self.hasvalue:
			return str(self.value)
		return '{}({})'.format(self.name, ', '.join(str(x) for x in self.args))

	def isconst(self, du):
		return self.hasvalue #maybe something with du?
