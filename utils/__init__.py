import asyncio
from .override import override
from .copy_doc import copydoc
from .final import final
from .complete import complete
future = asyncio.ensure_future
__all__ = ('override', 'copydoc', 'final', 'complete', 'future')