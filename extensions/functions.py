from typing import Any, Callable
import math

from .fancy_text import FancyText
from pymath2 import Undefined
from pymath2.builtins.variable import Variable
from pymath2.builtins.functions.unseeded_function import UnseededFunction
from pymath2.builtins.functions.seeded_function import SeededFunction
class SeededMathFunction(SeededFunction):
	@SeededFunction.value.getter
	def value(self):
		if not self.args[0].hasvalue:
			return Undefined
		else:
			return self.unseeded_base_object.func(self.args[0])
			# return super().value
	# @Override(Derivable)

	@property
	def hasvalue(self):
		return self.args[0].hasvalue

	def deriv(self, du: Variable) -> 'SeededFunction':
		return self.unseeded_base_object.deriv_w_args(du, self.args[0])

class MathFunction(UnseededFunction):
	seeded_type = SeededMathFunction
sin = MathFunction(name = 'sin', req_arg_len = 1, func = lambda a: math.sin(a))
cos = MathFunction(name = 'cos', req_arg_len = 1, func = lambda a: math.cos(a))
tan = MathFunction(name = 'tan', req_arg_len = 1, func = lambda a: math.tan(a))
csc = MathFunction(name = 'csc', req_arg_len = 1, func = lambda a: 1 / math.sin(a),)# (Undefined, 'x'), (Undefined, '1/sin(x)'))
sec = MathFunction(name = 'sec', req_arg_len = 1, func = lambda a: 1 / math.cos(a),)# (Undefined, 'x'), (Undefined, '1/cos(x)'))
cot = MathFunction(name = 'cot', req_arg_len = 1, func = lambda a: 1 / math.tan(a),)# (Undefined, 'x'), (Undefined, '1/tan(x)'))

ln = MathFunction(name = 'ln', req_arg_len = 1, func = lambda a: math.log(a))
log = MathFunction(name = 'log', req_arg_len = 1, func = lambda a: math.log10(a))
log2 = MathFunction(name = 'log2', req_arg_len = 1, func = lambda a: math.log2(a))

sqrt = MathFunction(name = 'sqrt', req_arg_len = 1, func = lambda a: math.sqrt(a))
fact = MathFunction(name = '!', req_arg_len = 1, func = lambda a: math.factorial(a))
gamma = MathFunction(name = 'gamma', req_arg_len = 1, func = lambda a: math.gamma(a))
Γ = gamma

# future: async lambda 
def derive(du, a): return cos(a) * a.deriv(du) #await
sin.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return -sin(a) * a.deriv(du) #await
cos.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return sec(a) ** 2 * a.deriv(du) #await
tan.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return -csc(a) * cot(a) * a.deriv(du) #await
csc.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return sec(a) * tan(a) * a.deriv(du) #await
sec.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return -csc(a) ** 2 * a.deriv(du) #await
cot.deriv_w_args = derive

# future: async lambda 
def derive(du, a): return a.deriv(du) / a #await
ln.deriv_w_args = derive

def derive(du, a): return .5 * a ** -.5 * a.deriv(du)
sqrt.deriv_w_args = derive
del derive

__all__ = tuple(x for x in list(locals()) if x[0] != '_' and type(x) != type)

