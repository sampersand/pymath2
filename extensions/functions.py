from typing import Any, Callable
import math

from .fancy_text import FancyText
from pymath2 import Undefined, override, complete
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
	# @override(Derivable)

	@override(SeededFunction)
	@property
	def hasvalue(self):
		return self.args[0].hasvalue

	@override(SeededFunction)
	async def _aderiv(self, du: Variable) -> 'SeededFunction':
		return await self.scrub(self.unseeded_base_object.deriv_w_args(du, self.args[0]))

class MathFunction(UnseededFunction):
	seeded_type = SeededMathFunction
sin = Undefined
cos = Undefined
tan = Undefined
csc = Undefined
sec = Undefined
cot = Undefined
ln = Undefined
log = Undefined
log2 = Undefined
sqrt = Undefined
fact = Undefined
gamma = Undefined

async def main():
	global sin
	global cos
	global tan
	global csc
	global sec
	global cot
	global ln
	global log
	global log2
	global sqrt
	global fact
	global gamma
	sin = await MathFunction.__anew__(MathFunction, name = 'sin', req_arg_len = 1, func = lambda a: math.sin(a))
	cos = await MathFunction.__anew__(MathFunction, name = 'cos', req_arg_len = 1, func = lambda a: math.cos(a))
	tan = await MathFunction.__anew__(MathFunction, name = 'tan', req_arg_len = 1, func = lambda a: math.tan(a))
	csc = await MathFunction.__anew__(MathFunction, name = 'csc', req_arg_len = 1, func = lambda a: 1 / math.sin(a),)# (Undefined, 'x'), (Undefined, '1/sin(x)'))
	sec = await MathFunction.__anew__(MathFunction, name = 'sec', req_arg_len = 1, func = lambda a: 1 / math.cos(a),)# (Undefined, 'x'), (Undefined, '1/cos(x)'))
	cot = await MathFunction.__anew__(MathFunction, name = 'cot', req_arg_len = 1, func = lambda a: 1 / math.tan(a),)# (Undefined, 'x'), (Undefined, '1/tan(x)'))

	ln = await MathFunction.__anew__(MathFunction, name = 'ln', req_arg_len = 1, func = lambda a: math.log(a))
	log = await MathFunction.__anew__(MathFunction, name = 'log', req_arg_len = 1, func = lambda a: math.log10(a))
	log2 = await MathFunction.__anew__(MathFunction, name = 'log2', req_arg_len = 1, func = lambda a: math.log2(a))

	sqrt = await MathFunction.__anew__(MathFunction, name = 'sqrt', req_arg_len = 1, func = lambda a: math.sqrt(a))
	fact = await MathFunction.__anew__(MathFunction, name = '!', req_arg_len = 1, func = lambda a: math.factorial(a))
	gamma = await MathFunction.__anew__(MathFunction, name = 'gamma', req_arg_len = 1, func = lambda a: math.gamma(a))
	# Γ = gamma

	# ensure_future: async lambda 
	async def derive(du, a): return cos(a) * await a._aderiv(du) #await
	sin.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return -sin(a) * await a._aderiv(du) #await
	cos.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return sec(a) ** 2 * await a._aderiv(du) #await
	tan.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return -csc(a) * cot(a) * await a._aderiv(du) #await
	csc.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return sec(a) * tan(a) * await a._aderiv(du) #await
	sec.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return -csc(a) ** 2 * await a._aderiv(du) #await
	cot.deriv_w_args = derive

	# ensure_future: async lambda 
	async def derive(du, a): return await a._aderiv(du) / a #await
	ln.deriv_w_args = derive

	async def derive(du, a): return .5 * a ** -.5 * await a._aderiv(du)
	sqrt.deriv_w_args = derive
	del derive
	return locals()
__all__ = tuple(str(x) for x in complete(main()))

