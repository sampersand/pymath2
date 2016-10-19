from pymath2 import Undefined
from .math_list import MathList
class AbstractPoint(MathList):
	pass
class Point2D(AbstractPoint):

	def __new__(cls, *args, isbase = False, **kwargs):
		return super().__new__(cls, *args, **kwargs)

	def __init__(self, *args, isbase = False, **kwargs):
		super().__init__(**kwargs)
		if __debug__:
			assert len(args) == 2
		super().__init__(*args)

		if isbase:
			self.x.name = 'x0'
			self.y.name = 'y0'

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

class Point3D(AbstractPoint):
	def __new__(cls, *args, isbase = False):
		return AbstractPoint.__new__(cls, *args)
	def __init__(self, *args, isbase = False):
		if __debug__:
			assert len(args) == 3
		super().__init__(*args)
		if isbase:
			self.x.name = 'x0'
			self.y.name = 'y0'
			self.z.name = 'z0'
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
