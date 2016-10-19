from pymath2 import Undefined, Constant, Variable
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
class MathList(list, NamedValuedObj):
	def scrub(self, arg):
		ret = super().scrub(arg)
		print(ret.__class__)
		if isinstance(ret, Constant):
			ret = Variable(value = ret.value)
		print(ret.__class__)
		return ret
	def __new__(self, *args, name = Undefined):
		return super().__new__(self, args)

	def __init__(self, *inps, name = Undefined):
		list.__init__(self, list(self.scrub(x) for x in inps))
		NamedValuedObj.__init__(self, name = name)

	@property
	def hasvalue(self):
		return all(x.hasvalue for x in self)
	@property
	def value(self):
		if not self.hasvalue:
			return Undefined
		return list(self)
