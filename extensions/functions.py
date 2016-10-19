from typing import Any, Callable
import math

from .fancy_text import FancyText
from pymath2 import Undefined
from pymath2.builtins.variable import Variable
from pymath2.builtins.functions.unseeded_function import UnseededFunction
from pymath2.builtins.functions.seeded_function import SeededFunction

class SeededMathFunction(SeededFunction):
	def __init__(self, math_instance: 'MathFunction', args: tuple) -> None:
		super().__init__(math_instance, args)


	@SeededFunction.value.getter
	def getter(self) -> Any:
		for arg in self.args: #async for
			if arg is Undefined or hasattr(arg, 'hasvalue') and not arg.hasvalue: #await
				return Undefined
		return super().value #await


	def deriv(self, du: Variable) -> SeededFunction:
		if __debug__:
			assert self.unseeded_base_object.derivative is not Undefined, 'No known way to take the derivative of ' + str(self)
		return self.unseeded_base_object.derivative(self, *self.args, du) #await

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
		return super().__str__() if self.fancy.has('args_str') else self.name

	def __repr__(self) -> str:
		return self.name
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

# future: async lambda 
def derive(self, a, du): return cos(a) * a.deriv(du) #await
sin.derivative = derive

# future: async lambda 
def derive(self, a, du): return -sin(a) * a.deriv(du) #await
cos.derivative = derive

# future: async lambda 
def derive(self, a, du): return sec(a) ** 2 * a.deriv(du) #await
tan.derivative = derive

# future: async lambda 
def derive(self, a, du): return -csc(a) * cot(a) * a.deriv(du) #await
csc.derivative = derive

# future: async lambda 
def derive(self, a, du): return sec(a) * tan(a) * a.deriv(du) #await
sec.derivative = derive

# future: async lambda 
def derive(self, a, du): return -csc(a) ** 2 * a.deriv(du) #await
cot.derivative = derive

# future: async lambda 
def derive(self, a, du): return a.deriv(du) / a #await
ln.derivative = derive

del derive

__all__ = tuple(x for x in list(locals()) if x[0] != '_' and type(x) != type)

