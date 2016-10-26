from typing import Any
from .objs.valued_obj import ValuedObj
from pymath2 import Undefined, override, inloop
class Number(ValuedObj):
	_valid_types = {int, float, complex, bool, type(Undefined)}
	@override(ValuedObj)
	async def __ainit__(self, value: Any = Undefined, **kwargs) -> None:
		assert inloop()
		if type(value) not in self._valid_types:
			raise TypeError('Cannot have type {} as a value for {}. Valid Types: {}'.format(
																		   type(value).__qualname__,
																		   type(self).__qualname__,
																		   self._valid_types, ))
		await super().__ainit__(value = value, **kwargs)
