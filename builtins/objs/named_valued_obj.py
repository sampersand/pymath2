from typing import Any
from pymath2 import Undefined, override
from .named_obj import NamedObj
from .valued_obj import ValuedObj
class NamedValuedObj(NamedObj, ValuedObj):

	@override(NamedObj, ValuedObj)
	async def __astr__(self) -> str:
		return await ValuedObj.__astr__(self) if await self._ahasvalue else await NamedObj.__astr__(self)

	@override(NamedObj, ValuedObj)
	async def __arepr__(self) -> str:
		name = future(self._aname)
		value = future(self._avalue)
		return '{}({}, {})'.format(self.__class__.__name__,
				(await self.async_getattr(await name))(),
				(await self.async_getattr(await value))())
