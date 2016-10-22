from typing import Any
from pymath2 import Undefined
class _fancy_stuff(dict):
	types = [list, tuple] #like this so it can easily be added to
	def __getattr__(self, attr: str) -> Any:
		return self[attr]
	def __setattr__(self, attr: str, value: Any) -> None:
		self[attr] = value
	def has(self, attr: str) -> bool:
		return attr in self and self[attr] is not Undefined

	def process(self, name, inp):
		if not isinstance(inp, tuple(_fancy_stuff.types)):
			return inp

		assert len(inp) == 2

		# if isinstance(inp, (list, tuple)):
		setattr(self, name, inp[1])
		return inp[0]
		# else:
		# 	if __debug__:
		# 		assert isinstance(inp, dict), type(inp)
		# 	setattr(self, name, inp['fancy'])
		# 	return inp['norm']

class FancyText():
	fancy = _fancy_stuff #used for proxies to types
	def __init__(self, **kwargs):
		self.fancy = _fancy_stuff(kwargs)

	def __getattribute__(self, attr):
		if attr in super().__getattribute__('fancy'):
			return getattr(super().__getattribute__('fancy'), attr)
		return super().__getattribute__(attr)