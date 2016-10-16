from .objs.math_obj import MathObj
from .objs.valued_obj import ValuedObj
class SeededDerivative():
	def __init__(self, n, d):
		self.n = n
		self.d = d
	@property
	def value(self): #everything is boilerplate here really....
		print("boilerplate: SeededDerivative.value")
		import asyncio
		async def foo():
			val = self.n.value.deriv(self.d.value)
			print("val:",val)
			awaited_val = await val
			print('awaited_val:', awaited_val)
			return awaited_val
		return asyncio.get_event_loop().run_until_complete(foo())
class Derivative(MathObj):
	def __init__(self, value):
		self.value = value
	def __truediv__(self, other):
		if not isinstance(other, Derivative):
			return NotImplemented
		return SeededDerivative(self, other)