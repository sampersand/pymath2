def check_final(parents, obj_or_name, do_crash):
	from .override import get_obj_name
	name = get_obj_name(obj_or_name)
	for parent in parents:
		assert hasattr(parent, obj_or_name)
		if hasattr(getattr(parent, obj_or_name), '_is_final'):
			if do_crash:
				raise TypeError('{} cannot be overriden!'.format(obj_or_name))
			return False
	return True
