from pymath2.exceptions import PyMath2Error
class NotDefinedError(PyMath2Error, ValueError):
	def __init__(self, not_defined_value):
		super().__init__()
		self._error = not_defined_value

	@property
	def message(self):
		return 'Undefined Value \'{}\'.'.format(self._error)