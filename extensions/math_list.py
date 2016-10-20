from pymath2 import Undefined, Constant, Variable, Override
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
class MathList(NamedValuedObj, list):

	print_parens = ('(', ')')

	@Override(list)
	def __new__(cls, list_args = (), name = Undefined):
		return super().__new__(cls, list_args)

	@Override(list, NamedValuedObj)
	def __init__(self, list_args = (), **kwargs):
		super().__init__(**kwargs)
		list.__init__(self, list(self.scrub(x) for x in list_args)) #baaad

	@Override(NamedValuedObj)
	def scrub(self, arg):
		ret = super().scrub(arg)
		if isinstance(ret, Constant):
			ret = Variable(value = ret.value)
		return ret

	@Override(NamedValuedObj)
	@NamedValuedObj.hasvalue.getter
	def hasvalue(self):
		return all(x.hasvalue for x in self)

	@Override(NamedValuedObj)
	@NamedValuedObj.value.getter
	def value(self):
		if not self.hasvalue:
			return Undefined
		return list(self)

	@Override(list, NamedValuedObj)
	def __str__(self):
		return '{}{}{}{}'.format(
			self.name,
			self.print_parens[0],
			', '.join(str(x) for x in self),
			self.print_parens[1])