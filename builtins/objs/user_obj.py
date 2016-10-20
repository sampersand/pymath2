from pymath2 import Undefined, Override
from .math_obj import MathObj
from inspect import stack
from re import search
class UserObj(MathObj):

	_parse_args_regex = Undefined

	@Override(MathObj)
	def __init__(self, *args, **kwargs) -> None:
		if __debug__:
			assert self._parse_args_regex is not Undefined, '_parse_args_regex cannot be undefined'
		parsed_args = self.parse_arg()
		kwargs.update(parsed_args) 
		super().__init__(*args, **kwargs)

	def parse_arg(self) -> dict:
		context = stack()[-1].code_context
		if __debug__:
			assert len(context) == 1, context #doesnt need to be, just havent seen an instance when it isnt
		context = context[0]
		match = search(self._parse_args_regex, context)
		if match == None:
			raise ValueError('No match found!')
		return self.process_match(match.groupdict())

	@staticmethod
	def process_match(match: dict) -> dict:
		return match