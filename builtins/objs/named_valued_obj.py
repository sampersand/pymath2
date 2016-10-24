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
		name = ensure_future(self._aname)
		value = ensure_future(self._avalue)
		return '{}({}, {})'.format(self.__class__.__name__,
				(await self.get_asyncattr(await name))(),
				(await self.get_asyncattr(await value))())
