from . import logger
from types import CoroutineType, FunctionType, GeneratorType, MethodType
from typing import Type, Callable, TypeVar, Any, Union
def get_obj_name(obj_or_name):
	""" Determine the name of the object """
	if isinstance(obj_or_name, str):
		name = obj_or_name
	elif type(obj_or_name) == staticmethod:
		name = obj_or_name.__func__.__name__
	elif type(obj_or_name) == property:
		name = get_obj_name(obj_or_name.fget)
	elif hasattr(obj_or_name, '__name__'):
		name = obj_or_name.__name__
	else:
		name = None
		logger.error('Couldnt determine a name for type {}'.format(type(obj_or_name)))
		return name
	assert name # there shouldn't be an empty name...
	logger.debug('Found a name for object of type {!s}: {!s}'.format(type(obj_or_name), name))
	return name

def _does_name_exist(classes, name, do_crash):
	"""
	determins if attribute name exists in every class.
	logger is implied if do_crash is false
	"""
	assert __debug__, 'Not required for this function, but parent functions should have checked'
	for cls in classes:
		assert isinstance(cls, type)
		if not hasattr(cls, name):
			err_str = '{} isnt overriding something with the same name in {}'.format(name, cls)
			logger.warning(err_str)
			if do_crash:
				raise AttributeError(err_str)
			assert not do_crash
			return False
	return True

from .copy_doc import copy_doc
from .check_final import check_final

T = TypeVar('T', CoroutineType, FunctionType, GeneratorType, MethodType, property, staticmethod, classmethod)
def override(*parents: Type[Any],
			 name: str = None,
			 do_crash: bool = None,
			 do_copy_doc: bool = True) -> Union[bool, None, Any]:
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
		name        -- The name to check. If left blank, a wrapper function will be returned, from
		               which name will be derived. (default: None)
		do_crash    -- If True, an AttributeError will be raised if name isn't found. Regardless, if
		               name isn't found, it will be logged.
		               (default: None --> False if name is specified, True otherwise)
		do_copy_doc -- If True, the documentation from the first parent's instance will be copied to 
		               the wrapper's argument. If a wrapper isn't used, this does nothing.
		               (default: True)
		check_final -- If True, this will make sure all the parent elements arent final.
		               (default: None --> False if name is specified, True otherwise)
    Returns:
    	True / False       -- If name was specified and do_crash is False, this will be whether or
		                      not name overrides everything.
    	None               -- If name was specified, and __debug__ is False.
    	Wrapper's Argument -- If the wrapper was used, this will return regardless of __debug__.


    Raises:
    	AttributeError -- If the name isn't found in the parent classes, and do_crash is True. Also,
    	                  if the wrapper's argument was supplied, but the name could not be ascertained.
    	ValueError     -- If the wrapper was used and a name wasn't able to be ascertained from the
    	                  passed argument.

	"""
	if not __debug__:
		logger.debug("Debug disabled, not checking existance of name {} in parent classes.".format(name))
		if name is not None:
			return None
		return lambda x: x #for thigns expecting a wrapper function (ie @overload)
	if name is not None:
		logger.debug("Name was supplied ({}). Using that".format(name))
		assert isinstance(name, str), 'Attributes are Strings!'
		return _does_name_exist(parents, name, False if do_crash == None else do_crash)

	def capture(inp_obj: T) -> T:
		""" Determine (if possible) inp_obj's name, copy doc if needed, and pass it to override ."""
		obj_name = get_obj_name(inp_obj)
		if obj_name == None:
			logger.error('Couldnt determine a name for type {}'.format(type(inp_obj)))
			raise AttributeError('Cannot find name for object type {}'.format(type(inp_obj)))
		exists = _does_name_exist(parents, obj_name, True if do_crash == None else do_crash)
		assert not do_crash or exists  #if do_crash is false, it doesnt matter if it exists
		if do_copy_doc:
			copy_doc(parents[0], inp_obj, obj_name)
			logger.debug("Copied doc from parent {} to object {}".format(parents[0], obj_name))
		if check_final:
			check_final(parents, obj_name, True if do_crash == None else do_crash)
		return inp_obj

	return capture







