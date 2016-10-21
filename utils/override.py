from types import CoroutineType, FunctionType, GeneratorType, MethodType
from typing import Type, Callable, TypeVar, Any, Union

def _get_obj_name(obj):
	""" Determine the name of the object """
	if type(obj) == staticmethod:
		return obj.__func__.__name__
	elif type(obj) == property:
		return _get_obj_name(obj.fget)
	elif hasattr(obj, '__name__'):
		return obj.__name__
	else:
		raise ValueError('No way to determine name for ' + str(obj.__class__))


def _determine_presence(classes, name):
	if not __debug__:
		return None
	for cls in classes:
		if name not in dir(cls):
			if do_crash:
				raise NameError('{} isnt overriding something with the same name in {}'.
								format(name, cls))
			return False # else
	return True

T = TypeVar('T', CoroutineType, FunctionType, GeneratorType, MethodType, property, staticmethod, classmethod)

def Override(*parents: Type[Any], name: str = None, do_crash: bool = True) -> Union[bool, None, Any]:
	"""
	Confirm that a method is overriding a method of the name in every parent.
	
	If name is None, a wrapper function (which will only accept one argument) will be returned.
	When this function is called (such as when Override is being used as a decorator), name will
	be ascertained.

	A few examples:

		class fruit():
			healthy = False
			def eat(): ...
			def __str__(self): ...
		class yellow():
			...
			def __str__(self): ...

		class bannana(fruit, yellow):

			@Override(fruit) # Won't crash
			def eat()... 

			@Override(fruit, yellow) # Won't crash
			def __str__(): ..

			@Override(fruit): # Will Crash
			def start_engine(): ...
	
	Override can also be used to check whether or not attributes are being overriden:

		class bananna(fruit, yellow):
			healthy = true
			Override(fruit, 'healthy') # Won't crash

	Note: if __debug__ is False, then this will simply return None or whatever object is captured, 
		  depending on whether or not 'name' was explicitly passed.

	Arguments:
		*parents -- A variable amount of classes that will be checked to make sure they have the 
		            correct name.
	Keyword Arguments:
		name     -- The name to check. If left blank, a wrapper function will be returned, from
		             which name will be derived. (default: None)
		do_crash -- If True, a NameError will be raised if name isn't found (default: False)

    Returns:
    	True / False       -- If name was specified and do_crash is False, this will be whether or
		                      not name overrides everything.
    	None               -- If name was specified, and __debug__ is False.
    	Wrapper's Argument -- If the wrapper was used, this will return regardless of __debug__.
    	The function (or name) that was passed to check

    Raises:
    	NameError  -- If the name isn't found in the parent classes, and do_crash is True.
    	ValueError -- If the wrapper was used and a name wasn't able to be ascertained from the
    	              passed argument.

	"""
	if name is not None:
		return _determine_presence(parents, name, do_crash)

	def capture(inp_obj: T) -> T:
		""" Determine (if possible) inp_obj's name, and pass it to Override."""
		_determine_presence(parents, _get_obj_name(inp_obj), do_crash)
		return inp_obj

	return capture


