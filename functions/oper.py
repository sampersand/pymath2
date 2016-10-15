from pymath2.functions.unseeded_function import unseeded_function
class oper(unseeded_function):
	def __init__(self, arg):
		super(oper, self).__init__()
		self.arg = arg

opers = {
	'__add__': lambda a, b: print('add:', a, b)
}
