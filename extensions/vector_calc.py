from pymath2 import UnseededFunction, Derivative
from .vector import Vector

def gradiant(args, func):
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

# gradiant = UnseededFunction(gradiant,
# 	'gradiant', '(x0, y0, ... n0), f',
# 	'<fx(x0, ...), fy(x0, ...), ..., fn(x0, ...)>', -1)


def dir_deriv(args, func, unit_vector):
	if __debug__:
		assert len(args) == len(unit_vector), 'len mismatch'
	return sum(gradiant(args, func).dot(unit_vector))

# dir_deriv = UnseededFunction(dir_deriv, 'dir_deriv', '(x0, y0, ...), f, u', 'gradiant((x0, y0, ...), f) · u', -1)
