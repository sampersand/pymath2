class MathObj():
	def __init__(self) -> None:
		pass

	@classmethod
	def generic_str(cls: type, prefix: str) -> str:
		return '{{{} {}}}'.format(prefix, cls.__qualname__)

	def __str__(self) -> str:
		return self.generic_str('default')

	def __repr__(self) -> str:
		return '{}()'.format(type(self).__qualname__)