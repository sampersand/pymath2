from typing import Any
from pymath2 import final
# @final
class UndefinedClass():
	async def __astr__(self) -> str: return 'Undefined'
	async def __arepr__(self) -> str: return '{}()'.format(self.__class__.__name__)

	async def __aadd__(self, other: Any) -> 'self': return self
	async def __asub__(self, other: Any) -> 'self': return self
	async def __amul__(self, other: Any) -> 'self': return self
	async def __atruediv__(self, other: Any) -> 'self': return self
	async def __afloordiv__(self, other: Any) -> 'self': return self
	async def __amod__(self, other: Any) -> 'self': return self
	async def __apow__(self, other: Any) -> 'self': return self

	async def __aradd__(self, other: Any) -> 'self': return self
	async def __arsub__(self, other: Any) -> 'self': return self
	async def __armul__(self, other: Any) -> 'self': return self
	async def __artruediv__(self, other: Any) -> 'self': return self
	async def __arfloordiv__(self, other: Any) -> 'self': return self
	async def __armod__(self, other: Any) -> 'self': return self
	async def __arpow__(self, other: Any) -> 'self': return self

	async def __aeq__(self, other: Any) -> bool: return other is self
	async def __ane__(self, other: Any) -> bool: return not (self == other)
	async def __alt__(self, other: Any) -> 'self': return self
	async def __agt__(self, other: Any) -> 'self': return self
	async def __ale__(self, other: Any) -> 'self': return self
	async def __agt__(self, other: Any) -> 'self': return self

	async def __aabs__(self) -> 'self': return self
	async def __aneg__(self) -> 'self': return self
	async def __apos__(self) -> 'self': return self
	async def __ainvert__(self) -> 'self': return self

	async def __aand__(self, other: Any) -> 'self': return self
	async def __aor__(self, other: Any) -> 'self': return self
	async def __axor__(self, other: Any) -> 'self': return self
	async def __alshift__(self, other: Any) -> 'self': return self
	async def __arshift__(self, other: Any) -> 'self': return self

	async def __arand__(self, other: Any) -> 'self': return self
	async def __aror__(self, other: Any) -> 'self': return self
	async def __arxor__(self, other: Any) -> 'self': return self
	async def __arlshift__(self, other: Any) -> 'self': return self
	async def __arrshift__(self, other: Any) -> 'self': return self

	async def __abool__(self) -> bool: return False
	# def __float__(self): raise AttributeError("Cannot take the f__float__")
	# def __int__(self): raise AttributeError("Cannot take the f__int__")
	# def __complex__(self): raise AttributeError("Cannot take the f__complex__")

	async def __await__(self) -> 'self': return self

	@property
	def hasvalue(self) -> bool:
		assert 0
		return complete(self._ahasvalue)

	@property
	async def _ahasvalue(self):
		return False

	async def deriv(self, du) -> 'self':
		return self

	def __hash__(self): return id(self)
Undefined = UndefinedClass()













