from typing import Any
from pymath2 import Derivative, Variable
from pymath2.builtins.functions.seeded_function import SeededFunction
from .functions import MathFunction
from .vector import Vector

def call(self, *args: tuple):
	return MathFunction.__call__(self, *args).value

class SeededVectorFunction(SeededFunction): #make this mathfunction
	@property
	def value(self):
		return super().value

class GradiantVector(MathFunction):
	seeded_type = SeededVectorFunction
	__call__ = call

	def __init__(self):
		super().__init__('gradiant', GradiantVector.calcval, 
			args_str = '(x0, y0, ... n0), f',
			body_str = '<fx(x0, ...), fy(x0, ...), ..., fn(x0, ...)>',
			req_arg_len = -1)

	@staticmethod
	def calcval(args, func):
		if __debug__:
			assert len(args), 'cannot have 0 args!'

		arg_iter = iter(args)
		
		for arg in args:
			arg._old_value = arg.value
			del arg.value #so it wont have a value and will be able to be derived
		
		ret = []
		for arg in arg_iter:
			ret.append((Derivative(func(*args)) / Derivative(arg)))
		for x in args:
			x.value = x._old_value
		return Vector(*ret)
gradiant = GradiantVector()


class DirDerivFunction(MathFunction):
	seeded_type = SeededVectorFunction
	__call__ = call
	def __init__(self):
		super().__init__('dir_deriv', DirDerivFunction.calcval, 
			args_str = '(x0, y0, ... n0), f, u',
			body_str = '<fx(x0, ...) * u.x, fy(x0, ...) * u.y, ..., fn(x0, ...) * u.n>',
			req_arg_len = -1)

	@staticmethod
	def calcval(args, func, unit_vector):
		if __debug__:
			assert len(args) == len(unit_vector), 'len mismatch'
		return sum(gradiant(args, func).dot(unit_vector))
dir_deriv = DirDerivFunction()
