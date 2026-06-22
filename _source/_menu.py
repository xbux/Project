import asyncio, os


NAME_ = ('  Heasi´s MS account factory \n')

class _MENU_:
    def __init__(self):
        self._confirmation_use_of_proxy_ = False
        
    def _clear_task_(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    async def main_menu_(self):
        self._clear_task_()
        
        print(NAME_)
        
        INFORMATION_ = (
            '[ This program automatically generate MS accounts' + '\n'
            '  Russian captcha solver on use' + '\n'
            '  Contact developer if want do any changes' + '\n' + '\n'
            
            '  Choices: [1 - Use proxy´s], [2 - Proxyless]' + '\n' + '\n'
            
            '  Residentials proxy´s are recommended for this process' + '\n'
            '  Note: Use proxyless mode can rate your own IP address ]' + '\n' + '\n')
        
        print(INFORMATION_)
        
        choice_ = input('  Method?: ')
        
        if choice_ not in ['1', '2']:
            for second_ in ['5', '4', '3', '2', '1']:
                print(f'  Wrong choice, continue in {second_}', end='\r', flush=True)
                await asyncio.sleep(1)
                
            self._clear_task_()
            return await self.main_menu_()
        
        if choice_ == '1':
            self._confirmation_use_of_proxy_ = True
            
        
        
_menu_ = _MENU_()