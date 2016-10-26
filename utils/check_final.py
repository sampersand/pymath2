from .override import get_obj_name
def check_final(parents, obj_or_name, do_crash):
	""" Check to make sure an object is not final. """
	name = get_obj_name(obj_or_name)
	for parent in parents:
		if hasattr(parent, '_is_final') and parent._is_final:
			if do_crash:
				raise TypeError('parent {} cannot be overriden!'.format(parent))
			return False

		assert hasattr(parent, obj_or_name)
		obj = getattr(parent, obj_or_name)
		if hasattr(obj, '_is_final') and obj._is_final and obj:
			if do_crash:
				raise TypeError('{} cannot be overriden!'.format(obj_or_name))
			return False
	return True
