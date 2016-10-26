
from pymath2 import Undefined, Constant, Variable, override, inloop
from pymath2.builtins.objs.named_valued_obj import NamedValuedObj
from pymath2.builtins.objs.math_obj import MathObj
class MathList(NamedValuedObj, list):
	def _gen_len_attr(*args):
		return {ele: pos for pos, val in enumerate(zip(*args)) for ele in val}
	_len_attrs = {} #would be like {1: ('x'), 2: ('x', 'y'), 3: ('i', 'j', 'k')}

	@override(NamedValuedObj)
	async def __anew__(cls, *args, name = Undefined, **kwargs):
		assert inloop()
		return super().__anew__(cls, *args, **kwargs)

	print_parens = ('(', ')')
	@override(NamedValuedObj)
	async def __ainit__(self, *args, **kwargs):
		assert inloop()
		super().__ainit__(**kwargs)
		argsl = [ensure_future(self.scrub(arg)) for arg in args]
		args = []
		for arg in argl:
			args.append(await arg)
		list.__init__(self, args) #baaad
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
	async def scrub(self, arg):
		assert inloop()
		ret = await super().scrub(arg)
		if isinstance(ret, Constant):
			ret = Variable(value = ret.value)
		return ret

	@override(NamedValuedObj)
	@NamedValuedObj.hasvalue.getter
	async def _ahasvalue(self):
		assert inloop()
		for x in self:
			if not await x._ahasvalue:
				return False
		return True

	@override(NamedValuedObj)
	@NamedValuedObj.value.getter
	async def _avalue(self):
		if not await self._ahasvalue:
			return Undefined
		return list(self)

	@override(NamedValuedObj)
	async def __astr__(self):
		return '{}{}{}{}'.format(
			await self._aname,
			self.print_parens[0],
			', '.join(self.list_str(self)),
			self.print_parens[1])

	@override(NamedValuedObj)
	async def __arepr__(self):
		return '{}({})'.format(self.__class__.__qualname__, ', '.join(self.list_str(self, repr = True)))

	@property
	def _len_attr(self) -> dict:
		return self._len_attrs[len(self)]

	@override(NamedValuedObj)
	async def __agetattr__(self, attr):
		try:
			ind = self._attrs_list_for_this_len[attr]
		except ValueError:
			pass
		else:
			return self[ind]
		return super().__agetattr__(attr)
	@override(NamedValuedObj)
	async def __asetattr__(self, attr, val):
		if attr not in self._attrs_list_for_this_len:
			return super().__asetattr__(attr, val)
		self[self._len_attr[attr]] = await self.scrub(val)






