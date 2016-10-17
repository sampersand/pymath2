from typing import Any
import math
from typing import Callable

from .fancy_text import FancyText
from pymath2 import Undefined
from pymath2.builtins.variable import Variable
from pymath2.builtins.functions.unseeded_function import UnseededFunction
from pymath2.builtins.functions.seeded_function import SeededFunction

class SeededMathFunction(SeededFunction):
	def __init__(self, math_instance: 'MathFunction', args: tuple) -> None:
		super().__init__(math_instance, args)


	@property
	def value(self) -> Any:
		if any(arg is Undefined or hasattr(arg, 'hasvalue') and not arg.hasvalue for arg in self.args):
			return Undefined
		return super().value


	async def deriv(self, du: Variable) -> SeededFunction:
		if __debug__:
			assert self.unseeded_base_object.derivative is not Undefined, 'No known way to take the derivative of ' + str(self)
		return await self.unseeded_base_object.derivative(*self.args, du)

class MathFunction(UnseededFunction, FancyText):
	seeded_type = SeededMathFunction
	def __init__(self,
				 name: [str] + FancyText.fancy.types,
				 wrapped_function: Callable,
				 args_str: [str] + FancyText.fancy.types = Undefined,
				 body_str: [str] + FancyText.fancy.types = Undefined,
				 req_arg_len: int = 1,
				 derivative: SeededFunction = Undefined) -> None:

		FancyText.__init__(self)
		UnseededFunction.__init__(self, wrapped_function, self.fancy.process('name', name),
				self.fancy.process('args_str', args_str), self.fancy.process('body_str', body_str))
		self._req_arg_len = req_arg_len
		self.derivative = derivative
		if __debug__:
			assert bool(args_str) == bool(body_str), 'cannot pass args and not a body!'
	@property
	def req_arg_len(self) -> int:
		return self._req_arg_len

	def __str__(self) -> str:
		return self._gen_unseeded_str(self.name, self.args_str, self.body_str) if self.fancy.has('args_str') else self.name

sin = MathFunction('sin', math.sin)
cos = MathFunction('cos', math.cos)
tan = MathFunction('tan', math.tan)
csc = MathFunction('csc', lambda a: 1 / math.sin(a), (Undefined, 'x'), (Undefined, '1/sin(x)'))
sec = MathFunction('sec', lambda a: 1 / math.cos(a), (Undefined, 'x'), (Undefined, '1/cos(x)'))
cot = MathFunction('cot', lambda a: 1 / math.tan(a), (Undefined, 'x'), (Undefined, '1/tan(x)'))

ln = MathFunction('ln', math.log)
log = MathFunction(('log', 'log₁₀'), math.log10)
log2 = MathFunction(('log2', 'log₂'), math.log2)

sqrt = MathFunction(('sqrt', '√'), math.sqrt)
fact = MathFunction('!', math.factorial)
gamma = MathFunction(('gamma', 'Γ'), math.gamma)
Γ = gamma

async def derive(a, du):
	return (cos(a)) * (await a.deriv(du))
	# cosa = cos(a)
	# aderiv = await a.deriv(du)
	# cosa_aderiv = cosa * aderiv
	# return cosa_aderiv
	# return cos(a) * await a.deriv(du)
sin.derivative = derive

async def derive(a, du): return -sin(a) * await a.deriv(du)
cos.derivative = derive

async def derive(a, du): return sec(a) ** 2 * await a.deriv(du)
tan.derivative = derive

async def derive(a, du): return -csc(a) * cot(a) * await a.deriv(du)
csc.derivative = derive

async def derive(a, du): return sec(a) * tan(a) * await a.deriv(du)
sec.derivative = derive

async def derive(a, du): return -csc(a) ** 2 * await a.deriv(du)
cot.derivative = derive

async def deriv(a, du): return await a.deriv(du) / a
ln.derivative = derive


__all__ = tuple(x for x in list(locals()) if x[0] != '_' and type(x) != type)