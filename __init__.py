# LOGGING_LEVEL = 'INFO'
LOGGING_LEVEL = 'DEBUG'
LOGGING_FORMAT = '[{asctime}][{levelname:<5}] {funcName:<15} :: {message}'
LOGGING_STYLE = '{'
import logging
logging.basicConfig(level = LOGGING_LEVEL, format = LOGGING_FORMAT, style = LOGGING_STYLE)

logger = logging.getLogger(__name__)

from .utils import *

def warnloop(logger, should_loop_exist = True):
	if inloop() != should_loop_exist:
		logger.warning('Should', '' if should_loop_exist else 'not', 'be in loop!', stack_info = True)

from .builtins.undefined import Undefined
from .builtins.constant import Constant, UserConstant as const
from .builtins.variable import Variable, UserVariable as var
from .builtins.derivative import Derivative, UserDerivative as d
from .builtins.functions.unseeded_function import UnseededFunction, UserFunction as func
# from .extensions import *

from .builtins.functions.operator import opers #to load up the main() function
del opers
from .extensions.functions import main
del main


logger.info('Done setting up.')
__all__ = tuple(x for x in tuple(locals()) if x[0] != '_')