from .pymath2_error import PyMath2Error
class NotDefinedError(PyMath2Error, ValueError):
	def __init__(self, undefined_value):
		self.undefined_value = undefined_value
		super().__init__('Undefined Value \'{}\'.'.format(self.undefined_value))
