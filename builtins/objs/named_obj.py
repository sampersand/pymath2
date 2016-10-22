from typing import Any 
from pymath2 import Undefined, override, final, future
from .math_obj import MathObj

class NamedObj(MathObj):
	@override(MathObj)
	async def __ainit__(self, name: str = Undefined, **kwargs) -> None:
		sini = future(super().__ainit__(**kwargs))
		name = future(self._aname_setter(name))
		await sini
		await name

	@final
	def name():
		@final
		def fget(self) -> (str, Undefined):
			return complete(self._aname)
		@final
		def fset(self, val: str) -> None:
			return complete(self._aname_setter(val))
		@final
		def fdel(self) -> None:
			return complete(self._aname_deleter(val)) #normally doesnt exist
		return locals()
	name = property(**name())

	@property
	async def _aname(self) -> (str, Undefined):
		return self._name

	async def _aname_setter(self, val: str) -> None:
		self._name = val

	@property
	@final
	def hasname(self) -> bool:
		return complete(self.hasname)

	@property
	async def _ahasname(self) -> bool:
		return await self._aname is not Undefined

	@override(MathObj)
	async def __astr__(self) -> str:
		hasname = future(self._ahasname)
		name = future(self._aname)
		return (await self.async_getattr(await name, '__str__'))()\
				if await hasname else self.generic_str(prefix = 'unnamed')

	@override(MathObj)
	async def __arepr__(self) -> str:
		name = (await self.async_getattr(await self._aname))()
		return '{}({})'.format(self.__class__.__name__, name)

	@override(MathObj)
	async def __aeq__(self, other: Any) -> bool:
		other = await self.scrub(other)
		if not hasattr(other, '_aname'):
			return False
		mname = future(self._aname)
		oname = future(other._aname)
		mname = await mname
		if mname == await oname and mname is not Undefined:
			return True
		return super().__aeq__(other)


