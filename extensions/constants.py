import math
from typing import Any
from pymath2 import Undefined
from pymath2.builtins.objs.named_obj import NamedObj
from pymath2.builtins.constant import Constant
from .fancy_text import FancyText
class MathConstant(Constant, NamedObj, FancyText):
	def __init__(self, name: [str] + FancyText.fancy.types, value: Any, **kwargs) -> None:
		# print('oh no')
		super().__init__()
		"""Note - this calls the valued constructor 3 times, and idk how to fix it."""
		FancyText.__init__(self)
		Constant.__init__(self, value)
		NamedObj.__init__(self, self.fancy.process('name', name))

	def __str__(self) -> str:
		return self.fancy.name if self.fancy.has('name') else self.name

	def __repr__(self) -> str:
		return '{}({!r}, {!r}{}'.format(
				type(self).__qualname,
				self.name, self.value,
				'' if not hasattr(self.fancy, 'name') else ', ' + repr(self.fancy.name))
pi = MathConstant(('pi', 'pi'), math.pi)
# pi = MathConstant(('pi', 'π'), math.pi)
e = MathConstant('e', math.e)
i = MathConstant('i', 1j)
golden_ratio = MathConstant(('phi','φ'), (1 + math.sqrt(5)) / 2, )