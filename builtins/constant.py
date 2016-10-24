from typing import Any
from pymath2 import Undefined, override, final, ensure_future
from .objs.valued_obj import ValuedObj
from .derivable import Derivable


class Constant(ValuedObj, Derivable):

	@override(Derivable)
	async def _aderiv(self, du: 'Variable') -> 0:
		return 0

	@override(ValuedObj)
	async def __arepr__(self) -> str:
		value = ensure_future(self._avalue)
		hasvalue = ensure_future(self._ahasvalue)
		return '{}({})'.format(self.__class__.__name__,
							   (await self.async_getattr(await value))() if await hasvalue else '')

@final
class UserConstant(Constant):
	@override(Constant)
	async def __ainit__(self, value):
		await super().__ainit__(value = value)