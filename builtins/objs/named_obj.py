from typing import Any 
from pymath2 import Undefined, override, final, ensure_future
from .math_obj import MathObj

class NamedObj(MathObj):
	@override(MathObj)
	async def __ainit__(self, name: str = Undefined, **kwargs) -> None:
		sini = await (super().__ainit__(**kwargs))
		name = ensure_future(self._aname_setter(name))
		# await sini
		await name

	@final
	def name():
		@final
		def fget(self) -> (str, Undefined):
			assert False, "don't use non-async functions!"
			return complete(self._aname)
		@final
		def fset(self, val: str) -> None:
			assert False, "don't use non-async functions!"
			return complete(self._aname_setter(val))
		@final
		def fdel(self) -> None:
			assert False, "don't use non-async functions!"
			return complete(self._aname_deleter(val)) #normally doesnt exist
		return locals()
	name = property(**name())

	@property
	async def _aname(self) -> (str, Undefined):
		return self._name

	async def _aname_setter(self, val: str) -> None:
		await self.__asetattr__('_name', val)

	# @property
	# @final
	# def hasname(self) -> bool:
	# 	return complete(self.hasname)

	@property
	async def _ahasname(self) -> bool:
		return await self._aname is not Undefined

	@override(MathObj)
	async def __astr__(self) -> str:
		hasname = ensure_future(self._ahasname)
		name = ensure_future(self._aname)
		return await self.async_getattr(await name, '__str__')\
				if await hasname else self.generic_str(prefix = 'unnamed')

	@override(MathObj)
	async def __arepr__(self) -> str:
		name = await self.async_getattr(await self._aname)
		return '{}({})'.format(self.__class__.__name__, name)

	@override(MathObj)
	async def __aeq__(self, other: Any) -> bool:
		other = await self.scrub(other)
		if not hasattr(other, '_aname'):
			return False
		mname = ensure_future(self._aname)
		oname = ensure_future(other._aname)
		mname = await mname
		if mname == await oname and mname is not Undefined:
			return True
		return super().__aeq__(other)


