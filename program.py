import asyncio, logging

from _source import *

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class _PROGRAM_:
    
    async def _initialize_program_(self):
        
        task_ = [_microsoft_._aiohttp_start_up_()
               for _ in range(_amount_)]
        
        await asyncio.gather(*task_)
        
        
        
        
        
        
_program_ = _PROGRAM_()
asyncio.run(_menu_.main_menu_())
_amount_ = int(input('  Amount: '))
print()
asyncio.run(_program_._initialize_program_())