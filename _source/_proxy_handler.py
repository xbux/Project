class _PROXY_HANDLER_:
    
    def __init__(self):
        self.proxy_list_ = [_.strip() for _ in open("_configuration/proxies.txt", encoding = 'utf-8') if _]
        self.proxy_index = -1
        
    def next_proxy_(self):
        self.proxy_index += 1
        if self.proxy_index >= len(self.proxy_list_):
            self.proxy_index = 0
        return self.proxy_list_[self.proxy_index]
    
    

_proxy_handler_ = _PROXY_HANDLER_()