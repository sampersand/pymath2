from .pymath2_error import PyMath2Error
class UnknownTypeError(PyMath2Error, TypeError):
	def __init__(self, unknown_type):
		self.unknown_type = unknown_type
		super().__init__("No known way to convert type '{}' into a MathObj".format(self.unknown_type))
