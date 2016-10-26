from . import logger
from typing import Type, Any, Union, TypeVar, Callable

from .override import get_obj_name
T = TypeVar('T')


def _override_doc(parent_class, obj, name):
	assert isinstance(parent_class, type)
	assert isinstance(name, str)
	assert hasattr(parent_class, name)

	parent_obj = getattr(parent_class, name)

	assert hasattr(parent_obj, '__doc__')

	obj.__doc__ = parent_obj.__doc__ # type: ignore name if name != None else get_obj_name(name))
	logger.debug("Copied doc: {}.__doc__ = {}.{}.__doc__".format(obj, parent_class, name))
def copy_doc(parent_class: Type, obj: T = None, name: str = None) -> Callable[[T], T]:
	if name != None and obj == None:
		raise ValueError('Cannot copy the doc of just a name - an object needs to be passed')
	assert name == None or obj != None
	if obj:
		_override_doc(parent_class, obj, name if name != None else get_obj_name(name))
		logger.debug("Copied doc: {}.__doc__ = {}.{}.__doc__".format(obj, parent_class, name))
		return 
	def capture(obj):
		_override_doc(parent_class, obj, get_obj_name(obj))
		logger.debug("Copied doc: {}.__doc__ = {}.{}.__doc__".format(obj, parent_class, name))
		return obj
	return capture


