from typing import Type, Any, Union, TypeVar, Callable

from .override import get_obj_name
T = TypeVar('T')


def _override_doc(parent_class, obj, name):
	assert hasattr(parent_class, name)

	parent_obj = getattr(parent_class, name)

	assert hasattr(parent_obj, '__doc__')

	obj.__doc__ = parent_obj.__doc__ # type: ignore name if name != None else get_obj_name(name))
def copy_doc(parent_class: Type, obj: T = None, name: str = None) -> Callable[[T], T]:
	assert name == None or obj != None, 'cannot pass one and not the other'

	if obj:
		_override_doc(parent_class, obj, name if name != None else get_obj_name(name))
		return 
	def capture(obj):
		_override_doc(parent_class, obj, get_obj_name(obj))
		return obj
	return capture


