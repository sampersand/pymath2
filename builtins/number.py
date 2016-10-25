from .objs.valued_obj import ValuedObj
from pymath2 import Undefined
class Number(ValuedObj):
	_valid_types = {int, float, complex, bool, type(Undefined)}