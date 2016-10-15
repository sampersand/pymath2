class PyMath2Error(Exception):
	def __init__(self, message: str = "Genderic PyMath2 Error.", ):
		self.message = message

	def __str__(self) -> str:
		return self.message
