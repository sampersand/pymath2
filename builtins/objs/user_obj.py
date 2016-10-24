from pymath2 import Undefined, override
from .math_obj import MathObj
from inspect import stack
from re import search
class UserObj(MathObj):

	_parse_args_regex = Undefined

	@override(MathObj)
	async def __ainit__(self, *args, override = False, **kwargs) -> None:
		assert self._parse_args_regex is not Undefined, '_parse_args_regex cannot be undefined'

		parsed_args = self.parse_arg(override)
		kwargs.update(parsed_args) 
		await super().__ainit__(*args, **kwargs)

	def parse_arg(self, override) -> dict:
		context = stack()[-1].code_context
		if not context:
			return {}
		assert len(context) == 1, context #doesnt need to be, just havent seen an instance when it isnt

		context = context[0]
		match = search(self._parse_args_regex, context)
		if match == None:
			if override:
				return {}
			raise ValueError('No match found!' + str(type(self)))

		return self.process_match(match.groupdict())

	@staticmethod
	def process_match(match: dict) -> dict:
		return match