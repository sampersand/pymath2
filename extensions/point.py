from pymath2 import Undefined
from .math_list import MathList
class Point(MathList):
	def x():
		def fget(self): return self[0]
		def fset(self, val): self[0] = val
		return locals()
	x = property(**x())
	def y():
		def fget(self): return self[1]
		def fset(self, val): self[1] = val
		return locals()
	y = property(**y())
	def z():
		def fget(self): return self[2]
		def fset(self, val): self[2] = val
		return locals()
	z = property(**z())