from . import logger
from typing import Any
from pymath2 import warnloop, Undefined, override, final, finish
from .objs.named_valued_obj import NamedValuedObj
from .objs.user_obj import UserObj
from .derivable import Derivable
from .number import Number
from pymath2 import inloop

class Variable(Number, NamedValuedObj):

	@override(Derivable)
	async def _aisconst(self, du: 'Variable') -> bool:
		warnloop(logger)
		assert inloop()
		return self is not du and self.name != du.name

	@override(Derivable)
	async def _aderiv(self, du: 'Variable') -> (0, 1):
		warnloop(logger)
		assert inloop()
		return await self.scrub(int(not await self._aisconst(du)))

@final
class UserVariable(UserObj, Variable):
	@override(Variable)
	async def __ainit__(self, name = Undefined, value = Undefined, **kwargs):
		await super().__ainit__(value = value, name = name, **kwargs)

	@override(NamedValuedObj)
	async def __arepr__(self) -> str:
		async with finish() as f:
			name = f.future(self._aname)
			value = f.future(self._avalue)
			hasvalue = f.future(self._ahasvalue)
			prname = f.future(self.get_asyncattr(await name))
			prvalue = 'value=' + await self.get_asyncattr(await value) if await hasvalue else Undefined
			return '{}({})'.format(self.__class__.__name__, 
				', '.join(x for x in ('myname', prvalue) if x is not Undefined))

