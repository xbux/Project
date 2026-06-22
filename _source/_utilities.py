import random, faker, datetime

temporal_ = faker.Faker()

class _UTILITIES_:
    def __init__(self):
        self.current_account_ = ''
        self.temporal_data_ = ''
        self.temporal_canary_ = ''
        
    def collect_all_parameters_(self, data_from_response_):
        self.set_current_credentials_()
        birth_date_ = str(temporal_.date_between(start_date = '-50y', end_date = '-20y')).split('-')
        
        self.temporal_data_ = {
        'BirthDate': f'{birth_date_[2]}:{birth_date_[1]}:{birth_date_[0]}',
        'CheckAvailStateMap': [self.current_account_['email'] + ':false'],
        'Country': 'US',
        'EvictionWarningShown': [],
        'FirstName': temporal_.name().replace(' ', ''),
        'IsRDM': False,
        'HFId': data_from_response_.split('"sHipFid":"')[1].split('","')[0],
        'IsOptOutEmailDefault': True,
        'IsOptOutEmailShown': 1,
        'IsOptOutEmail': True,
        'IsUserConsentedToChinaPIPL': False,
        'LastName': temporal_.last_name(),
        'LW': 1,
        'MemberName': self.current_account_['email'],
        'RequestTimeStamp': f'{str(datetime.datetime.utcnow().isoformat()[:-3])}Z',
        'ReturnUrl': '',
        'SignupReturnUrl': '',
        'SuggestedAccountType': 'EASI',
        'SiteId': data_from_response_.split('"sSiteId":"')[1].split('","')[0],
        'VerificationCode': '',
        'VerificationCodeSlt': '',
        'WReply': '',
        'MemberNameChangeCount': 1,
        'MemberNameAvailableCount': 1,
        'MemberNameUnavailableCount': 0,
        'Password': self.current_account_['password'],
        'uiflvr': 1001,
        'scid': int(data_from_response_.split('"iScenarioId":')[1].split(',')[0]),
        'uaid': 'dfae82c0cac540619b66b25e3706b808',
        'hpgid': 200225 }
        
  
    def build_email_(self):
        random_number_ = str(random.randint(1000000000, 9999999999))
        name_ = str(temporal_.name()).replace(' ', '')
        separator_ = random.choice(['.', '_', '-'])
        return f'heasi{separator_}{random_number_}{separator_}{name_}@outlook.com'.lower()
        
    def build_password_(self):
        character_ = random.choice(['/', '!', '%', '&'])
        random_number_ = str(random.randint(10000, 99999))
        name_ = str(temporal_.name()).replace(' ', '')[::-1]
        return f'{character_}{random_number_}{name_}{random_number_[::-1]}{character_}'
    
    def set_current_credentials_(self):
        email_, password_ = self.build_email_(), self.build_password_()
        
        self.current_account_ = {
            'email': email_,
            'password': password_ }
        
    def encode_decode_string_(self, content_):
        encode_decode_ = content_.encode().decode('unicode-escape')
        
        return encode_decode_
    
    def return_agent_(self):
        agent_ = temporal_.user_agent()
        
        return agent_
    
    def save_in_file_(self, _content_, _file_name_):
        with open(_file_name_, 'a', encoding = 'utf-8') as file:
            file.write(f'{_content_}\n')
        
        
_utilities_ = _UTILITIES_()
