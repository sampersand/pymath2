
from pymath2 import Undefined, Constant, Variable, override
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.objs.math_obj import MathObj
class MathList(NamedValuedObj, list):
	def _gen_len_attr(*args):
		return {ele: pos for pos, val in enumerate(zip(*args)) for ele in val}
	_len_attrs = {} #would be like {1: ('x'), 2: ('x', 'y'), 3: ('i', 'j', 'k')}

	@override(list)
	def __new__(cls, *args, name = Undefined, **kwargs):
		return super().__new__(cls, *args, **kwargs)

	print_parens = ('(', ')')
	@override(NamedValuedObj, list)
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		list.__init__(self, list(self.scrub(x) for x in args)) #baaad
		for attr_name in self._attrs_list_for_this_len:
			attr = getattr(self, attr_name)
			if not attr.hasname:
				attr.name = '{}_for_{}'.format(attr_name, id(self))

	@property
	def _attrs_list_for_this_len(self) -> dict:
		return self._len_attrs.get(len(self), {})

	@property
	def attrs(self) -> dict:
		return {val: getattr(self, val) for val in self._attrs_list_for_this_len}
	@override(NamedValuedObj)
	def scrub(self, arg):
		ret = super().scrub(arg)
		if isinstance(ret, Constant):
			ret = Variable(value = ret.value)
		return ret

	@override(NamedValuedObj)
	@NamedValuedObj.hasvalue.getter
	def hasvalue(self):
		return all(x.hasvalue for x in self)

	@override(NamedValuedObj)
	@NamedValuedObj.value.getter
	def value(self):
		if not self.hasvalue:
			return Undefined
		return list(self)

	@override(NamedValuedObj, list)
	def __str__(self):
		return '{}{}{}{}'.format(
			self.name,
			self.print_parens[0],
			', '.join(str(x) for x in self),
			self.print_parens[1])

	@override(NamedValuedObj, list)
	def __repr__(self):
		return '{}({})'.format(self.__class__.__qualname__, ', '.join(repr(x) for x in self))

	@property
	def _len_attr(self) -> dict:
		return self._len_attrs[len(self)]


	def __getattr__(self, attr):
		try:
			ind = self._attrs_list_for_this_len[attr]
		except ValueError:
			pass
		else:
			return self[ind]
		return super().__getattr__(attr)

	def __setattr__(self, attr, val):
		if attr not in self._attrs_list_for_this_len:
			return super().__setattr__(attr, val)
		self[self._len_attr[attr]] = self.scrub(val)






