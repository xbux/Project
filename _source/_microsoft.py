import asyncio, aiohttp, uuid, json, codecs

from ._utilities import _utilities_
from ._captcha_solver import _captcha_solver_
from ._proxy_handler import _proxy_handler_
from ._menu import _menu_


class _MICROSOFT_:
    
    def __init__(self):
        self.base_url_ = 'https://signup.live.com:443/'
        
        self.tries_ = 0
        self.success_ = 0
        
    def process_sign_up_assessment_(self, assessment_parameters_):
        process_data_ = json.loads(assessment_parameters_)
        process_data_ = {keys_: codecs.decode(values_, 'unicode-escape') 
         for keys_, values_ in process_data_.items()}
        
        return process_data_
    
    
    async def get_text_response_(self, _session_, aiohttp_proxy_):
        async with _session_.get(self.base_url_ + f'signup?lic=1&uaid={uuid.uuid4()}',
                                 proxy = aiohttp_proxy_) as _response_:
            data_from_response_ = await _response_.text()
            canary_ = data_from_response_.split('"apiCanary":"')[1].split('"')[0]
            #url_dfp_ = data_from_response_.split('"urlDfp":"')[1].split('"')[0]
            
            _utilities_.temporal_canary_ = canary_
            _utilities_.collect_all_parameters_(data_from_response_)
            
            #await self.dfp_(_session_, url_dfp_)
            
            
    async def authorization_for_email_availability_(self, _session_, aiohttp_proxy_):
        await self.get_text_response_(_session_, aiohttp_proxy_)
        
        headers_ = {
            'correlationId': _utilities_.temporal_data_['uaid'],
            'client-request-id': _utilities_.temporal_data_['uaid'],
            'canary': _utilities_.encode_decode_string_(_utilities_.temporal_canary_)}
        
        json_ = {
            'clientExperiments': [{
               'parallax': 'enablejspublickeydeprecationexperiment',
               'control': 'enablejspublickeydeprecationexperiment_control',
               'treatments': [
                 'enablejspublickeydeprecationexperiment_treatment' ]}]}
        
        async with _session_.post(self.base_url_ + 'API/EvaluateExperimentAssignments',
                                  headers = headers_,
                                  json = json_,
                                  proxy = aiohttp_proxy_) as _response_:
            print(_response_)
            if _response_.status == 200:
                data_from_response_ = await _response_.json()
                canary_ = data_from_response_['apiCanary']
                _utilities_.temporal_canary_ = canary_
            
            
    async def get_confirmation_if_email_available_(self, _session_, aiohttp_proxy_):
        await self.authorization_for_email_availability_(_session_, aiohttp_proxy_)
        
        headers_ = {
            'correlationId': _utilities_.temporal_data_['uaid'],
            'client-request-id': _utilities_.temporal_data_['uaid'],
            'canary': _utilities_.encode_decode_string_(_utilities_.temporal_canary_)}
        
        json_ = {
            'includeSuggestions': False,
            'signInName': _utilities_.temporal_data_['MemberName'],
            'uiflvr': 1001,
            'scid': _utilities_.temporal_data_['scid'],
            'uaid': _utilities_.temporal_data_['uaid'],
            'hpgid': 200225}
        
        async with _session_.post(self.base_url_ + 'API/CheckAvailableSigninNames?lic=1&uaid=' + _utilities_.temporal_data_['uaid'],
                                  headers = headers_,
                                  json = json_,
                                  proxy = aiohttp_proxy_) as _response_:
            
            data_from_response_ = await _response_.text()
            
            if 'isAvailable' in data_from_response_:
                canary_ = data_from_response_.split('"apiCanary":"')[1].split('"')[0].replace('\\', '')
                _utilities_.temporal_canary_ = canary_
                await self.create_account_(_session_, aiohttp_proxy_)
               
    async def create_account_(self, _session_, aiohttp_proxy_):
        json_ = _utilities_.temporal_data_

        headers_ = {
            'correlationId': _utilities_.temporal_data_['uaid'],
            'Content-Length': str(len(str(json_))),
            'client-request-id': _utilities_.temporal_data_['uaid'],
            'canary': _utilities_.encode_decode_string_(_utilities_.temporal_canary_)}
       
        async with _session_.post(self.base_url_ + 'API/CreateAccount?lic=1&uaid=' + _utilities_.temporal_data_['uaid'],
                                  headers = headers_,
                                  json = json_,
                                  proxy = aiohttp_proxy_) as _response_:
            
            data_from_response_ = await _response_.json()
            print(data_from_response_)
            getting_error_ = data_from_response_['error']['code']
            if getting_error_ == '1041':
                assessment_parameters_ = data_from_response_['error']['data']
                await self.finish_process_(_session_, assessment_parameters_, aiohttp_proxy_)
                
    async def finish_process_(self, _session_, assessment_parameters_, aiohttp_proxy_):
        process_data_ = self.process_sign_up_assessment_(assessment_parameters_)
        
        await _captcha_solver_.set_aiohttp_()
        await _captcha_solver_.start_call_for_solution_(), await _captcha_solver_.get_solution_()
        
        _utilities_.temporal_data_['HPId'] = 'B7D8911C-5CC8-A9A3-35B0-554ACEE604DA'
        _utilities_.temporal_data_['HSol'] = _captcha_solver_.solution_
        _utilities_.temporal_data_['HType'] = 'enforcement'
        _utilities_.temporal_data_['HId'] = _captcha_solver_.solution_
        _utilities_.temporal_data_['RiskAssessmentDetails'] = process_data_['riskAssessmentDetails']
        _utilities_.temporal_data_['RepMapRequestIdentifierDetails'] = process_data_['repMapRequestIdentifierDetails']
        
        json_ = _utilities_.temporal_data_

        headers_ = {
            'correlationId': _utilities_.temporal_data_['uaid'],
            'Content-Length': str(len(str(json_))),
            'client-request-id': _utilities_.temporal_data_['uaid'],
            'canary': _utilities_.encode_decode_string_(_utilities_.temporal_canary_)}
       
        async with _session_.post(self.base_url_ + 'API/CreateAccount?lic=1&uaid=' + _utilities_.temporal_data_['uaid'],
                                  headers = headers_,
                                  json = json_,
                                  proxy = aiohttp_proxy_) as _response_:

            data_from_response_ = await _response_.text()
            
            if 'redirectUrl' in data_from_response_:
                _content_ = f"{_utilities_.current_account_['email']}:{_utilities_.current_account_['password']}"
                print(f" Account Created: {_content_}\n Using Proxy: {aiohttp_proxy_}")
                _utilities_.save_in_file_(_content_, '_credentials/accounts.txt')
 
    async def _aiohttp_start_up_(self):
        try:
            if _menu_._confirmation_use_of_proxy_:
                aiohttp_proxy_ = 'http://' + _proxy_handler_.next_proxy_()
                
            if not _menu_._confirmation_use_of_proxy_:
                aiohttp_proxy_ = None
                
            aiohttp_connector_ = aiohttp.TCPConnector(ssl = False, limit = 0)
            async with aiohttp.ClientSession(trust_env = True,
                                             connector = aiohttp_connector_) as _session_:
                
                await self.get_confirmation_if_email_available_(_session_,
                                                                aiohttp_proxy_)
        except Exception as e:print(e)
            
    
            
_microsoft_ = _MICROSOFT_()
asyncio.run(_microsoft_._aiohttp_start_up_())