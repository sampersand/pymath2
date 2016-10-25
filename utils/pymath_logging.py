
from inspect import stack, isframe
import logging
# from .inloop import inloop
FORMAT = '[{asctime}][{levelname}] {func_name:10}: {message}'
pymath_logging = logging.getLogger('pymath')
pymath_handler = logging.Handler()
pymath_handler.setFormatter(FORMAT)
# pymath_logging.setHandler(
# pymath_logging.
# quit()
pymath_handler.setLevel(0)
# if __debug__:
# 	logging.basicConfig(level=10, format = FORMAT, style = '{')
def _log_stuff(log_func, message, stack_level = 2, **kwargs):
	s = stack()
	assert len(s) >= stack_level
	fr = s[stack_level]
	assert isframe(fr)
	log_func(message, extra = {'func_name': fr.fr_code.__name__}, **kwargs)
def debug(*messages, sep = ' ', logger = None, **kwargs):
	pymath_logging.debug(sep.join(messages), **kwargs)
	# logging.getLogger(logger).debug(sep.join(messages), **kwargs)

def debugf(formatter, *messages, logger = None, **kwargs):
	pymath_logging.debug(formatter.format(*messages, **kwargs), **kwargs)
	# logging.getLogger(logger).debug(formatter.format(*messages, **kwargs), **kwargs)

def warn(*messages, sep = ' ',logger = None, **kwargs):
	pymath_logging.warn(sep.join(messages), **kwargs)
	# logging.getLogger(logger).warn(sep.join(messages), **kwargs)

def warnf(formatter, *messages, logger = None, **kwargs):
	pymath_logging.warn(formatter.format(*messages, **kwargs), **kwargs)
	# logging.getLogger(logger).warn(formatter.format(*messages, **kwargs), **kwargs)

def warnloop(should_loop_exist = True):
	if inloop() != should_loop_exist:
		warn('Should not be in loop!', stack_info = True)

__all__ = ('debug', 'debugf', 'warn', 'warnf', 'warnloop')