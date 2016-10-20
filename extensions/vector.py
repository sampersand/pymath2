from pymath2 import Undefined, Constant
from .math_list import MathList
class Vector(MathList):
	def __abs__(self):
		return abs(sum(x.value ** 2 for x in self) ** .5)

	print_parens = ('<', '>')

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
		return sum(x[0] * x[1] for x in zip(self, other))

	def __mul__(self, other):
		other = self.scrub(other)
		if hasattr(other, 'hasvalue') and other.hasvalue:
			return Vector(*(d * other for d in self))



	def x():
		def fget(self):
			return self[0]
		def fset(self, val):
			self[0].value = val
		return locals()
	x = property(**x())

	def y():
		def fget(self):
			return self[1]
		def fset(self, val):
			self[1].value = val
		return locals()
	y = property(**y())

	def z():
		def fget(self):
			return self[2]
		def fset(self, val):
			self[2].value = val
		return locals()
	z = property(**z())

