import aiohttp, json

class _CAPTCHA_SOLVER_:
    
    def __init__(self):
        self.api_key_ = open('_configuration/captcha_key_.heasi').read()
        
        self.captcha_host_ = 'api.crazytoken.ru/'
        
        self.temporal_session_ = None
        
        self.taskID_ = ''
        
        self.solution_ = ''
        
    async def set_aiohttp_(self):
        aiohttp_connector_ = aiohttp.TCPConnector(ssl = False, limit = 0)
        
        self.temporal_session_ = aiohttp.ClientSession(trust_env = True,
                                         connector = aiohttp_connector_)
        
        
    async def get_balance_(self):
        url_ = 'https://' + self.captcha_host_ + f'balance?apikey={self.api_key_}'
        async with self.temporal_session_.get(url_) as _response_:
            
            data_from_response_ = await _response_.text()
            
            if 'OK' in data_from_response_:
                data_from_response_ = json.loads(data_from_response_)
                print(f'{data_from_response_["balance"]}')
                return f'{data_from_response_["balance"]}'
        
    async def start_call_for_solution_(self):
        url_ = 'https://' + self.captcha_host_ + 'createTask'
        json_data_ = {
              'apikey': self.api_key_,
              'sitekey': 'B7D8911C-5CC8-A9A3-35B0-554ACEE604DA' }
        
        async with self.temporal_session_.post(url_,
                                               json = json_data_) as _response_:
            
            data_from_response_ = await _response_.text()

            if 'OK' in data_from_response_:
                data_from_response_ = json.loads(data_from_response_)
                self.taskID_ = data_from_response_['task_id']
                
    async def get_solution_(self):
        for _ in range(50):
            
            url_ = 'https://' + self.captcha_host_ + 'getTaskResult'
            json_data_ = {
                  'apikey': self.api_key_,
                  'task_id': self.taskID_ }
            
            async with self.temporal_session_.post(url_, 
                                                  json = json_data_) as _response_:
                
                data_from_response_ = await _response_.text()

                if 'OK' in data_from_response_:
                    data_from_response_ = json.loads(data_from_response_)
                    self.solution_ = data_from_response_['result']['token']
                    return True
                
        return False
                
            
        
_captcha_solver_ = _CAPTCHA_SOLVER_() 

       
       