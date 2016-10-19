from pymath2 import Derivative, Variable
from .functions import MathFunction
class Du_fFunction(MathFunction):
	def __init__(self):
		super().__init__('Du_f', Du_fFunction.calcval, 
			args_str = '(x0, y0, ... n0), f, u',
			body_str = '<fx(x0, ...), fy(x0, ...), ..., fn(x0, ...)>',
			req_arg_len = -1)

	@staticmethod
	def calcval(args, func, unit_vector):
		if __debug__:
			assert len(args), 'cannot have 0 args!'
			assert len(unit_vector) == len(args), 'length mismatch between unit_vector and args!'

		arg_iter = iter(args)
		unit_iter = iter(unit_vector)
		
		for arg in args:
			arg._old_value = arg.value
			del arg.value #so it wont have a value and will be able to be derived
		
		ret = Derivative(func(*args)) / Derivative(next(arg_iter)) * next(unit_iter)
		for arg in arg_iter:

			ret += (Derivative(func(*args)) / Derivative(arg)) * next(unit_iter)
		for x in args:
			x.value = x._old_value
		return ret

Du_f = Du_fFunction()
