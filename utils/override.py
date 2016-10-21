from types import CoroutineType, FunctionType, GeneratorType, MethodType
from typing import Type, Callable, TypeVar, Any, Union
def get_obj_name(obj):
	""" Determine the name of the object """
	if type(obj) == staticmethod:
		return obj.__func__.__name__
	elif type(obj) == property:
		return get_obj_name(obj.fget)
	elif hasattr(obj, '__name__'):
		return obj.__name__
	else:
		print(dir(obj))
		raise ValueError('No way to determine name for ' + str(obj.__class__))


def _determine_presence(classes, name, do_crash):
	if not __debug__:
		return None
	for cls in classes:
		if not hasattr(cls, name):
			if do_crash:
				raise NameError('{} isnt overriding something with the same name in {}'.
								format(name, cls))
			return False # else
	return True

T = TypeVar('T', CoroutineType, FunctionType, GeneratorType, MethodType, property, staticmethod, classmethod)
from .copy_doc import copydoc
def override(*parents: Type[Any],
			 name: str = None,
			 do_crash: bool = None,
			 copy_doc: bool = True) -> Union[bool, None, Any]:
	"""
	Confirm that a method is overriding a method of the name in every parent.
	
	If name is None, a wrapper function (which will only accept one argument) will be returned.
	When this function is called (such as when override is being used as a decorator), name will
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

			@override(fruit) # Won't crash
			def eat()... 

			@override(fruit, yellow) # Won't crash
			def __str__(): ..

			@override(fruit): # Will Crash
			def start_engine(): ...
	
	override can also be used to check whether or not attributes are being overriden:

		class bananna(fruit, yellow):
			healthy = true
			assert override(fruit, 'healthy') # Won't crash

	Note: if __debug__ is False, then this will simply return None or whatever object is captured, 
		  depending on whether or not 'name' was explicitly passed.

	Arguments:
		*parents -- A variable amount of classes that will be checked to make sure they have the 
		            correct name.
	Keyword Arguments:
		name     -- The name to check. If left blank, a wrapper function will be returned, from
		             which name will be derived. (default: None)
		do_crash -- If True, a NameError will be raised if name isn't found
		            (default: None --> False if name is specified, True otherwise)
		copy_doc -- If True, the documentation from the first parent's instance will be copied to 
		            the wrapper's argument. If a wrapper isn't used, this does nothing.
		            (default: True)
    Returns:
    	True / False       -- If name was specified and do_crash is False, this will be whether or
		                      not name overrides everything.
    	None               -- If name was specified, and __debug__ is False.
    	Wrapper's Argument -- If the wrapper was used, this will return regardless of __debug__.


    Raises:
    	NameError  -- If the name isn't found in the parent classes, and do_crash is True.
    	ValueError -- If the wrapper was used and a name wasn't able to be ascertained from the
    	              passed argument.

	"""
	if name is not None:
		return _determine_presence(parents, name, False if do_crash == None else do_crash)

	def capture(inp_obj: T) -> T:
		""" Determine (if possible) inp_obj's name, copy doc if needed, and pass it to override ."""
		obj_name = get_obj_name(inp_obj)
		_determine_presence(parents, obj_name, True if do_crash == None else do_crash)
		if copy_doc:
			copydoc(parents[0], inp_obj, obj_name)
		return inp_obj

	return capture