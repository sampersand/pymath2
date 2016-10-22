def final(obj):
	if isinstance(obj, type):
		for attr_name in dir(obj):
			try:
				attr = getattr(obj, attr_name)
				print(attr_name)
				if attr_name in {'__class__', '__bases__', '__base__'}:
					continue
				res_attr = final(attr)
				setattr(obj, attr_name, res_attr)
			except AttributeError:pass
	print(type(obj))
	obj._is_final = True
	return obj