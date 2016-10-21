def check_final(parents, obj_or_name, do_crash):
	from .override import get_obj_name
	name = get_obj_name(obj_or_name)
	for parent in parents:
		if __debug__:
			assert isinstance()