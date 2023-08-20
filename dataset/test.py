def foo():
	try:
		1/0
	except Exception:
		pass
foo()