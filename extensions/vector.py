from pymath2 import Undefined
from .math_list import MathList
class Vector(MathList):
	def __abs__(self):
		return abs(sum(x.value ** 2 for x in self) ** .5)

	def __str__(self):
		return '<{}>'.format(', '.join(str(x) for x in self)) 

	@property
	def unit(self):
		#TODO: define name
		self_val = abs(self)
		return Vector(*(x / self_val for x in self), name = Undefined)

	@staticmethod
	def from_points(p1, p2):
		if p1.name is Undefined or p2.name is Undefined:
			name = Undefined
		else:
			name = '{}{}_'.format(p1.name, p2.name)
		return Vector(*(x[1] - x[0] for x in zip(p1, p2)), name = name)

	def deriv(self, du):
		return Vector(*(arg.deriv(du) for arg in self))

	def dot(self, other):
		return Vector(*(x[0] * x[1] for x in zip(self, other)))