from pymath2.functions import UnseededFunction
class Operator(UnseededFunction):
	def __init__(self, arg):
		self.arg = arg

opers = {
	'__add__': lambda a, b: print('add:', a, b)
}
