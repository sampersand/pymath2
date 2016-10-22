import asyncio
from .override import override
from .copy_doc import copy_doc
from .final import final
from .complete import complete
future = asyncio.ensure_future
__all__ = ('override', 'final', 'complete', 'future', 'copy_doc')