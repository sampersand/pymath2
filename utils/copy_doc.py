from typing import Type, Any, Union, TypeVar, Callable

from .override import get_obj_name
T = TypeVar('T')


def _override_doc(parent_class, obj, name):
	if __debug__:
		from .override import override
		assert override(parent_class, name = name)
	parent_obj = getattr(parent_class, name)
	if __debug__:
		assert hasattr(parent_obj, '__doc__')
	obj.__doc__ = parent_obj.__doc__
		# type: ignore name if name != None else get_obj_name(name))
def copydoc(parent_class: Type, obj: T = None, name: str = None) -> Callable[[T], T]:
	if __debug__:
		assert name == None or obj != None, 'cannot pass one and not the other'
	if obj:
		_override_doc(parent_class, obj, name if name != None else get_obj_name(name))
		return 
	def capture(obj):
		_override_doc(parent_class, obj, get_obj_name(obj))
		return obj
	return capture


