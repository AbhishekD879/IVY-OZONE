import calendar
import json
import logging
import random
import string
import lxml.html
from collections import namedtuple
from crlat_core.datatypes.dict_keys_to_properties import DictKeysToProperties
from faker import Faker
from crlat_gvc_wallet_client import LOGGER_NAME
from crlat_gvc_wallet_client.utils.exceptions import GVCUserClientException
from crlat_gvc_wallet_client.utils.request.request import GVCUserClientRequest
from crlat_gvc_wallet_client.utils.settings import define_gvc_settings
from crlat_gvc_wallet_client.utils.settings import get_gvc_settings


class GVCUserClient(object):
    def __init__(self, env='tst2', brand='bma', env_host = None):
        self.env = env
        self.brand = brand
        self.env_host = env_host
        define_gvc_settings(backend=self.env, brand=brand, env_host=self.env_host)
        self.gvc_settings = get_gvc_settings()
        self._logger = logging.getLogger(LOGGER_NAME)
        self.request = GVCUserClientRequest(hostname=self.gvc_settings.config.mobileportal,
                                            use_session=True)

    # registration
    def _generate_username(self) -> str:
        """
        Generate unique username
        :return: Username
        """
        chars = string.ascii_uppercase + string.digits
        postfix = ''.join(random.choice(chars) for _ in range(7))

        return f'{self.gvc_settings.registration_prefix}{postfix}'

    @staticmethod
    def _generate_email(username) -> str:
        """
        Generate unique email address based on username
        :param username: Username
        :return: email
        """
        return f'test+{username}@internalgvc.com'

    def registration(self, username: str = None, **kwargs):
        """
        Main registration request with all user-related entered data
        http://qa2.www.coral.co.uk/en/mobileportal/api/Registration
        """
        f = Faker()
        username = username if username else self._generate_username()
        emailaddress = kwargs.get('emailaddress', self._generate_email(username))
        captchaResponse = '' if self.env not in ['prod', 'beta'] else '03AGdBq24rr3wePVWEV_nm6ULVcoN2ANXvZkVbSr2bmrWB9HAb8UhT0QnlSQJwVPdcm7r1s7wqwXLbd0QGQEB'
        data = {
            'captchaResponse': captchaResponse,
            'requestData':
                {
                    'addresscountrycode': kwargs.get('addresscountrycode', 'GB'),
                    'currencycode': kwargs.get('currencycode', 'GBP'),
                    'emailaddress': emailaddress,
                    'username': username,
                    'password': kwargs.get('password', 'Qwerty19'),
                    'gender': kwargs.get('gender', 'Male'),
                    'firstname': kwargs.get('firstname', f.first_name_female()),
                    'lastname': kwargs.get('lastname', f.last_name_female()),
                    'dateofbirth': kwargs.get('dateofbirth', f.date(pattern='%Y-%m-%d', end_datetime='-22y')),
                    'addressfinder': kwargs.get('addressfinder', f.city()),
                    'addressline1': kwargs.get('addressline1', f.street_address()),
                    'addresscity': kwargs.get('addresscity', 'London'),
                    'addresszip': kwargs.get('addresszip', 'W1U 8ED'),
                    'mobilenumber': kwargs.get('mobilenumber', '7537152317'),
                    'mobilecountrycode': kwargs.get('mobilecountrycode', '44'),
                    'promotionsswitch': True,
                    'optionsSelected': [
                        {
                            'key': 'Email',
                            'name': 'Email',
                            'selected': False
                        },
                        {
                            'key': 'SMS',
                            'name': 'SMS',
                            'selected': False
                        },
                        {
                            'key': 'Phone call',
                            'name': 'Phone',
                            'selected': False
                        },
                        {
                            'key': 'Post',
                            'name': 'RegularMail',
                            'selected': False
                        }
                    ],
                    'tacacceptance': kwargs.get('tacacceptance', True),
                    'bonustrackerid': 0,
                    'addressstate': 'ZZ',
                    'isFastRegistration': False,
                    'productName': "SPORTSBOOK"
                }
        }
        self._logger.debug(f'{json.dumps(data, indent=2)}')
        user_data = DictKeysToProperties(**data.get('requestData'))
        data = json.dumps(data)
        uri_path = 'Registration/CreateAccount'
        self.request.post(url=uri_path,
                          data=data,
                          timeout=20)  # increased default timeout due to KYC verification
        return user_data

    def update_personal_details(self, **kwargs):
        """
        Implements request to update user's personal details.
        Better to use after request that gets all user's personal details
        :param kwargs: user's data
        """
        session_token = self.get_logged_user_api_tokens().session_token

        extra_headers = {
            'X-XSRF-TOKEN': session_token,
        }

        data = {
            'address1': kwargs.get('address1'),
            'address2': kwargs.get('address2'),
            'city': kwargs.get('city'),
            'country': kwargs.get('country'),
            'email': kwargs.get('email'),
            'firstname': kwargs.get('firstname'),
            'gender': kwargs.get('gender'),
            'lastname': kwargs.get('lastname'),
            'mobilecountrycode': kwargs.get('mobilecountrycode'),
            'mobilenumber': kwargs.get('mobilenumber'),
            'phonecountrycode': kwargs.get('phonecountrycode'),
            'phonenumber': kwargs.get('phonecountrycode'),
            'state': kwargs.get('state'),
            'title': kwargs.get('title'),
            'zip': kwargs.get('zip')
        }

        data = json.dumps(data)

        return self.request.post(f'{self.gvc_settings.config.mobileportal}PersonalDetails',
                                 extra_headers=extra_headers,
                                 data=data,
                                 verify=False)

    def funds_regulation_data(self, **kwargs):
        """
        Request to set limits after register for Ladbrokes GVC Wallet
        http://qa2.myaccount.ladbrokes.com/en/mobileportal/api/lcgaccountupgrade/PostFundsRegulationData
        http://qa2.www.coral.co.uk/en/mobileportal/api/lcgaccountupgrade/PostFundsRegulationData
        """
        limit_type = kwargs.get('limit_type', 'NoLimit')
        skip_limit = True if limit_type == 'NoLimit' else False
        data = {
            'FundProtection': True,
            'SkipLimits': skip_limit,
            'LimitType': limit_type,
            'RequestedDailyLimit': kwargs.get('daily_limit', 0),
            'RequestedWeeklyLimit': kwargs.get('weekly_limit', 0),
            'RequestedMonthlyLimit': kwargs.get('monthly_limit', 0),
        }

        extra_headers = {
            'X-XSRF-TOKEN': kwargs.get('session_token'),
        }

        self._logger.debug(f'{json.dumps(data, indent=2)}')
        user_data = DictKeysToProperties(**data)
        data = json.dumps(data)
        self.request.post(url='lcgaccountupgrade/PostFundsRegulationData',
                              data=data,
                              extra_headers=extra_headers)
        return user_data

    def screen_name(self, nickname: str, sso_token: str):
        """
        Request to set nickname for different games
        http://qa2.myaccount.ladbrokes.com/en/mobileportal/api/ScreenName

        :param nickname: User's nickname
        :param sso_token: User's single sign on token (or named as X-XSRF-TOKEN)
        """
        nickname = nickname.replace(self.gvc_settings.registration_prefix,
                                    self.gvc_settings.nickname_prefix)

        extra_headers = {
            'X-XSRF-TOKEN': sso_token,
        }

        data = {
            'nickname': nickname
        }
        data = json.dumps(data)

        response = self.request.post(url='ScreenName', data=data, extra_headers=extra_headers)
        return response

    def finalize_workflow(self, sso_token: str):
        """
        Request for finalizing registration  after all submitted registration data
        http://qa2.sports.coral.co.uk/en/labelhost/api/finalizeWorkflow
        :param sso_token: User's single sign on token (or named as X-XSRF-TOKEN)
        """
        cookies_dict = self.request.session.cookies.get_dict()
        # These Changes Are with Respect to Auth token Change in the Cookies
        if not cookies_dict:
            # Checks If cookies exist
            raise GVCUserClientException("Not Able to Get Cookies After Login")
        if cookies_dict.get('vauth'):
            # Checks If vauth token exist on cookies
            vauth = cookies_dict.get('vauth')
            vauth = 'vauth=' + vauth
        elif cookies_dict.get('vnauth'):
            # Checks If vnauth token exist on cookies
            vnauth = cookies_dict.get('vnauth')
            vauth = 'vnauth=' + vnauth
        else:
            # Throws Exception if Auth Token Is Not Present in cookies
            return GVCUserClientException("Not able to get Vauth or Vnauth token from cookies")

        extra_headers = {
            'x-bwin-browser-url': self.gvc_settings.config.base_host_url + 'en/mobileportal/lcgfundsregulation',
            'Referer': self.gvc_settings.config.base_host_url + 'en/mobileportal/lcgfundsregulation',
            'X-XSRF-TOKEN': sso_token,
            'Set-Cookie': vauth,
            'Content-Length': '2'
        }

        data = {}
        self.request.post(url=f'{self.gvc_settings.config.labelhost}finalizeworkflow',
                          extra_headers=extra_headers, timeout=5, data=json.dumps(data))

    def login(self, username: str, password: str = 'Qwerty19', **kwargs):
        """
        Same request as UI Login into app
        >>> self.login(username='Cool-user-14', password='123pass')
        """
        captcharesponse = '' if self.env not in ['prod', 'beta'] else '03AGdBq27rEqb0W0yWVq8cH5CCfcplEI'
        data = {
            'username': username,
            'password': password,
            'captcharesponse': captcharesponse,
            'rememberme': kwargs.get('rememberme', False),
            'brandId': None
        }
        data = json.dumps(data)
        request = self.request.post(url=f'{self.gvc_settings.config.labelhost}login',
                                    data=data)
        return request.json()

    def register_new_user(self, username: str = None, **kwargs) -> namedtuple:
        """
        General shortcut with all actions required for user to be threaten as registered on site
        :param username: Username. If None – will be generated on-the-fly
        :param kwargs: Any parameters for ``registration`` and ``funds_regulation_data`` methods. e.g.;
        >>> self.register_new_user(username='supa_user_02',
        >>>                            gender='Male',
        >>>                            daily_limit=50)
        :return: Named Tuple with user info fields
        Usage:
        >>> user_info = self.register_new_user()
        >>> username, password = user_info.username, user_info.password
        """
        self.request.session.cookies.clear()  # user should not be logged in for API registration

        registration = self.registration(username=username, **kwargs)

        session_token = self.get_logged_user_api_tokens().session_token

        funds_regulation = self.funds_regulation_data(session_token=session_token, **kwargs)
        if registration.addresscountrycode == 'GB':
            self.finalize_workflow(sso_token=session_token)

        _user_info = namedtuple('user_info', ['username',
                                              'password',
                                              'emailaddress',
                                              'currencycode',
                                              'daily_limit',
                                              'weekly_limit',
                                              'monthly_limit'
                                              ])
        user_info = _user_info(username=registration.username,
                               password=registration.password,
                               emailaddress=registration.emailaddress,
                               currencycode=registration.currencycode,
                               daily_limit=funds_regulation.RequestedDailyLimit,
                               weekly_limit=funds_regulation.RequestedWeeklyLimit,
                               monthly_limit=funds_regulation.RequestedMonthlyLimit)

        self._logger.info(f'*** Registered new user with params: {json.dumps(user_info._asdict(), indent=2)}')
        return user_info

    def change_password(self, old_password: str, new_password: str = 'Qwerty19'):
        """
        Request: http://qa2.sports.coral.co.uk/en/labelhost/api/changepassword
        Method to change password
        :param old_password: old password value
        :param new_password: new password value
        """
        data = {
            'newpassword': new_password,
            'oldpassword': old_password,
        }
        data = json.dumps(data)
        self.request.post(url=f'changepassword',
                          data=data)

    # ---------------   DEPOSIT   ------------------- #

    def quick_deposit_enabled(self):
        """
        Method implements request that verified availability quick deposit for logged in user
        https://beta-sports.coral.co.uk/en/labelhost/api/menu/QuickDepositEnabled

        :return: True if response text equal to 'true', False otherwise
        """
        url = f'{self.gvc_settings.config.base_host_url}en/labelhost/api/menu/QuickDepositEnabled'

        response = self.request.get(url=url)
        return response.text == 'true'

    def client_config_partial_logged_user_api_tokens(self) -> dict:
        """
        Get response with authorization tokens

        :return: Response as dict with user tokens
        """
        header = {
            'Accept-Language': 'en-US'
        }

        params = (
            ('configNames', 'vnUser'),
            ('configNames', 'vnClaims'),
            ('configNames', 'vnBalanceProperties')
        )
        url = f'{self.gvc_settings.config.base_host_url}en/api/clientconfig/partial'

        response = self.request.get(url=url, params=params, extra_headers=header, timeout=20)

        resp_dict = json.loads(response.text)
        self._logger.debug(f'{json.dumps(resp_dict, indent=2)}')

        return resp_dict

    def get_logged_user_api_tokens(self) -> namedtuple:
        """
        Retrieve user's authorization tokens

        :return: Dict with user's authorization tokens
        """
        base_url = self.gvc_settings.config.deposit_user_api_tokens

        resp_dict = self.client_config_partial_logged_user_api_tokens()

        session_token = resp_dict['vnClaims'][f'{base_url}sessiontoken']
        sso_token = resp_dict['vnClaims'][f'{base_url}ssotoken']
        user_token = resp_dict['vnClaims'][f'{base_url}usertoken']

        _auth_tokens = namedtuple('auth_tokens', ['session_token',
                                                  'sso_token',
                                                  'user_token']
                                  )
        user_info = _auth_tokens(session_token=session_token,
                                 sso_token=sso_token,
                                 user_token=user_token)

        return user_info

    def auth_user_in_payment_service(self, username: str, sso_token: str):
        """
        Retrieve user's authorization token

        :param username: User's name
        :param sso_token: User's authorization SSO token
        :return: Response
        """
        username = f'{self.gvc_settings.auth_username_prefix}{username}'
        #url = f'{self.gvc_settings.config.cashier_host}paymentservice/authentication/authenticateUser'
        url = f'{self.gvc_settings.config.cashier_host}commonservice/authentication/authenticateUser'

        headers = {
            'sso-key': sso_token
        }

        data_params = {
            'userId': username,
            'labelInfo':
                {
                    'brandId': self.gvc_settings.config.brand_id,
                    'productId': self.gvc_settings.config.product_id,
                    'channelId': self.gvc_settings.config.channel_id
                }
        }
        data = json.dumps(data_params)

        return self.request.post(url=url, extra_headers=headers, data=data)

    def get_user_auth_token(self, username: str, sso_token: str) -> str:
        """
        Retrieve user's authorization token

        :param username: User's name
        :param sso_token: User's authorization SSO token
        :return: User's authorization token
        """
        response = self.auth_user_in_payment_service(username=username, sso_token=sso_token)

        auth_code = response.headers._store.get('auth-code')[1]

        return auth_code

    def get_deposit_instruments_for_payment_service(self, auth_token: str):
        """
        Cashier payment account info

        :param auth_token: User's authorization token
        :return: Response
        """
        url = f'{self.gvc_settings.config.cashier_host}paymentservice/deposit/qdinstruments'

        headers = {
            'auth-code': auth_token,
        }

        response = self.request.get(url=url, extra_headers=headers, timeout=15)

        return response

    def get_deposit_payment_ids(self, auth_token: str) -> namedtuple:
        """
        Cashier payment account info

        :param auth_token: User's authorization token
        :return: Cashier payment account info:
                    - CC ID
                    - Payment account ID
                    - Payment account update URL
        """
        deposit_instruments = self.get_deposit_instruments_for_payment_service(auth_token=auth_token)
        response_text = json.loads(deposit_instruments.text)

        self._logger.debug(f'{json.dumps(response_text, indent=2)}')

        if not isinstance(response_text, list) or not response_text:
            self._logger.info(f'{json.dumps(response_text, indent=2)}')
            raise GVCUserClientException('No payment methods for user')

        card = response_text[0]

        cc_id = card['paymentAccountInfo']['id']
        payment_account_id = card['paymentAccountInfo']['paymentAccountId']
        payment_account_update_url = card['paymentAccountInfo']['paymentAccountUpdateUrl']
        payment_method = card['paymentMethodInfo']['paymentMethod']

        _payment_ids = namedtuple('payment_ids', ['cc_id',
                                                  'payment_account_id',
                                                  'payment_account_update_url',
                                                  'payment_method']
                                  )

        payment_ids = _payment_ids(cc_id=cc_id,
                                   payment_account_id=payment_account_id,
                                   payment_account_update_url=payment_account_update_url,
                                   payment_method=payment_method)

        return payment_ids

    def cc_delete_submit_action(self, **kwargs):
        """
        Request URL: https://cashier.coral.co.uk/deposit/ccDeleteSubmit.action

        :param kwargs: card_number, card_type, session_key, j_session_id, cc_id
        :return: Response
        """
        cookies = {
            'sessionKey': kwargs.get('session_key'),
            'JSESSIONID': kwargs.get('j_session_id'),
        }

        card_type = kwargs.get('card_type')

        if card_type == 'visa':
            cardtype = 'VISA'
            preference = 'VISA'
        elif card_type == 'mastercard':
            cardtype = 'MC'
            preference = 'MASTERCARD'
        else:
            raise GVCUserClientException('Payment card type is not supported, please add support')

        data = {
            'cc': kwargs.get('cc_id'),
            'cardnumber': kwargs.get('card_number'),
            'cardtype': cardtype,
            'maskRequest': 'Y',
            'preference': preference
        }

        return self.request.session.post(f'{self.gvc_settings.config.cashier_host}deposit/ccDeleteSubmit.action',
                                         data=data,
                                         cookies=cookies,
                                         headers=self.request.headers)

    def delete_payment_card(self, username, card_number, card_type):
        """
        Remove payment card for user

        :param username: Username
        :param card_number: in format "5137 xxxx xxxx 6224"
        :param card_type: "visa"/"mastercard"
        """
        tokens = self.get_logged_user_api_tokens()
        sso_token = tokens.sso_token

        auth_token = self.get_user_auth_token(username=username,
                                              sso_token=sso_token)

        payment_ids = self.get_deposit_payment_ids(auth_token=auth_token)

        self.create_cashier_session(sso_token)
        j_session_id = self.request.session.cookies.get_dict().get('JSESSIONID')

        return self.cc_delete_submit_action(card_number=card_number,
                                            card_type=card_type,
                                            session_key=sso_token,
                                            j_session_id=j_session_id,
                                            cc_id=payment_ids.cc_id)

    def create_cashier_session(self, session_key: str):
        """
        This request will create cashier session for currently logged in user.
        In result of execution "JSESSIONID" token will be generated.

        :param session_key: Session key (SSOToken)
        :return: Request response
        """
        url = f'{self.gvc_settings.config.cashier_host}deposit/depositOptionsMerchant.action'

        params = (
            ('sessionKey', session_key),
            ('LANG_ID', 'en'),
            ('parent', f'{self.gvc_settings.config.base_host_url}en'),
            ('trid', 'in11135'),
        )

        return self.request.get(url=url, params=params)

    def initialize_deposit_method(self, j_session_id: str, deposit_method='mastercard'):
        """
        Send request to initialize chosen deposit method, it will return HTML page with necessary information

        :param j_session_id: Specified deposit method to initialize (e.g. 'mastercard', 'maestro', 'visa')
        :param deposit_method: Specified deposit method to initialize (e.g. 'mastercard', 'maestro', 'visa')
        :return: Initialized deposit method, e.g. request response
        """
        cookies = {
            'JSESSIONID': j_session_id,
        }

        return self.request.get(url=f'{self.gvc_settings.config.cashier_host}deposit/{deposit_method}Used.action',
                                cookies=cookies)

    def _parse_deposit_method(self, deposit_page: str) -> namedtuple:
        """
        Parse and fetch needed information for initialized deposit method

        :param deposit_page: Initialized deposit method page, as simple text
        :return: Parsed information:
                    - url to add new card
                    - card holder name
        """
        site = lxml.html.fromstring(deposit_page)

        token = site.xpath('.//div[@id="token"]')
        if not token:
            raise GVCUserClientException('Cannot get Card URL')
        card_url = token[0].text
        try:
            card_holder_name = site.xpath('.//input[@id="nameoncard"]')[0].value
        except Exception:
            user_info = self.client_config_partial_logged_user_api_tokens().get('vnClaims')
            name = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname'
            surname = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname'
            card_holder_name = f'{user_info.get(name)} {user_info.get(surname)}'
        try:
            ccguid = site.xpath('.//input[@id="ccguid"]')[0].value
        except Exception:
            ccguid = None

        _parsed_info = namedtuple('parsed_info', ['card_url',
                                                  'card_holder_name',
                                                  'ccguid']
                                  )

        parsed_info = _parsed_info(card_url=card_url,
                                   card_holder_name=card_holder_name,
                                   ccguid=ccguid)

        return parsed_info

    def fetch_cashier_card_data(self, session_id: str, deposit_method) -> namedtuple:
        """
        This method creates Cashier payment session, initializes specified Deposit payment method
        and retrieves URL to add new card and card holder name

        :param session_id: Session ID
        :param deposit_method: Specified deposit method to initialize (e.g. 'mastercard', 'maestro', 'visa')
        :return: Parsed information:
                    - url to add new card
                    - card holder name
        """
        self.create_cashier_session(session_id)

        j_session_id = self.request.session.cookies.get_dict().get('JSESSIONID')
        deposit_page = self.initialize_deposit_method(j_session_id=j_session_id, deposit_method=deposit_method)

        return self._parse_deposit_method(deposit_page.text)

    def get_bwin_ccguid_for_new_card(self,
                                     card_url: str,
                                     card_number: str,
                                     expiry_month: str,
                                     expiry_year: str,
                                     cvv: str,
                                     name_on_card: str):
        """
        This method generates ccGUID data for initial deposit
        Should be used only for https://ngpg.bwin.com/api/

        :param card_url: URL for request to add new card.
        :param card_number: Card number, e.g. 5190023456735555
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param name_on_card: Card holder's name
        :return: ccGUID data
        """
        data_params = {
            'cardNumber': card_number,
            'expiryMonth': expiry_month,
            'expiryYear': expiry_year,
            'cvv': cvv,
            'nameOnCard': name_on_card
        }
        data = json.dumps(data_params)

        response = self.request.put(url=card_url, data=data)
        resp_dict = json.loads(response.text)

        return resp_dict

    def get_kalixa_ccguid_for_new_card(self,
                                       card_url: str,
                                       card_number: str,
                                       expiry_month: str,
                                       expiry_year: str,
                                       cvv: str,
                                       name_on_card: str):
        """
        This method generates ccGUID data for initial deposit.
        Should be used only for https://api.test.kalixa.com/api/

        :param card_url: URL for request to add new card.
        :param card_number: Card number, e.g. 5190023456735555
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param name_on_card: Card holder's name
        :return: ccGUID data
        """
        # url format - https://api.test.kalixa.com/api/v4/merchants/PG/users/61463032/accounts/9ff29faa-b66f-404d-8142-cf2eb7632e0e?token=XXXX
        acc_id = card_url.split('accounts/')[-1].split('?token=')[0]

        data_params = {
            'id': acc_id,
            'type': '1',
            'cardNumber': card_number,
            'cardVerificationCode': cvv,
            'expiryMonth': expiry_month,
            'expiryYear': expiry_year,
            'holderName': name_on_card,
            'visible': True
        }

        data = json.dumps(data_params)

        response = self.request.put(url=card_url, data=data)
        resp_dict = json.loads(response.text)

        return resp_dict

    def get_ccguid_for_new_card(self,
                                card_url: str,
                                card_number: str,
                                expiry_month: str,
                                expiry_year: str,
                                cvv: str,
                                name_on_card: str):
        """
        This method calls defined request based on chosen API. Currently supported the following API's:
            - https://api.test.kalixa.com/api/
            - https://ngpg.bwin.com/api/
            - https://releaseb-ngpg.ivycomptech.co.in/api/

        :param card_url: URL for request to add new card.
        :param card_number: Card number, e.g. 5190023456735555
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param name_on_card: Card holder's name
        :return: ccGUID data
        """
        if 'kalixa' in card_url:
            return self.get_kalixa_ccguid_for_new_card(card_url=card_url,
                                                       card_number=card_number,
                                                       expiry_month=expiry_month,
                                                       expiry_year=expiry_year,
                                                       cvv=cvv,
                                                       name_on_card=name_on_card)
        elif 'ngpg' in card_url:
            return self.get_bwin_ccguid_for_new_card(card_url=card_url,
                                                     card_number=card_number,
                                                     expiry_month=expiry_month,
                                                     expiry_year=expiry_year,
                                                     cvv=cvv,
                                                     name_on_card=name_on_card)
        else:
            raise GVCUserClientException('Current ccGUID API provider is not supported. Please implement support.'
                                             f'\n Provider url:\n {card_url}')

    def deposit_via_new_card(self,
                             amount: str,
                             card_type: str,
                             card_number: str,
                             expiry_month: str,
                             expiry_year: str,
                             cvv: str,
                             cashier_card_data: namedtuple,
                             **kwargs):
        """
        Make initial deposit with new card for user for specified amount

        :param amount: Amount to deposit
        :param card_type: Card type, e.g. visa, mastercard
        :param card_number: Card number, e.g. 5190023456735555
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param cashier_card_data: Parsed cashier card data from response
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        name_on_card = cashier_card_data.card_holder_name

        ccguid = cashier_card_data.ccguid
        card_url = cashier_card_data.card_url
        resp_dict = ''
        if not ccguid or card_url.startswith('https'):
            resp_dict = self.get_ccguid_for_new_card(card_url=card_url,
                                                     card_number=card_number,
                                                     expiry_month=expiry_month,
                                                     expiry_year=expiry_year,
                                                     cvv=cvv,
                                                     name_on_card=name_on_card)

            ccguid = resp_dict['accounts'][0]['id']

        month_abbr = calendar.month_abbr[int(expiry_month)].upper()
        currency = kwargs.get('currency', 'GBP')

        if card_type == 'mastercard':
            card_params = {
                'card_type': 'MC',
                'cardtype': 'MC',
                'preference': 'MASTERCARD',
                'oldPreference': 'MASTERCARD',
            }
        elif card_type == 'visa':
            card_params = {
                'card_type': 'VISA',
                'cardtype': 'VISA',
                'preference': 'VISA',
                'oldPreference': 'VISA',
            }
        else:
            card_params = {}

        params = {
            'userConsent': 'true',
            'submitaction': 'ccInputGuidSubmit.action',
            'playPlusBinCheckEnabled': 'false',
            'maskRequest': 'Y',
            'ccguid': ccguid,
            'tokenErrorResonse': '',
            'tokenErrorCode': '',
            'cardResponseFromProvider': resp_dict,
            'payrcardBins': '459651',
            'paymentAccountTypeID': '',
            'stressEnabled': 'N',
            'formattedMinTxnLimit': '5.00',
            'formattedMaxTxnLimit': '10000.00',
            'formattedFee': '0.00',
            'feeType': 'abs',
            'currency': currency,
            'navamount': amount,
            'amount': amount,
            'cc': '',
            'nameoncard': name_on_card,
            'expirydate': f'{expiry_month}/{expiry_year[-2:]}',
            'month': month_abbr,
            'year': expiry_year[-2:],
            'cvv2': '',
            'bonusId': '',
            'tncFromBonusService': 'Y',
            'newBonusEnabled': 'true',
            'showBonusQualifyMsg': 'Y',
            'showPaypalBonusMsg': 'Y',
            'bonuscode': ''
        }
        params.update(card_params)

        return self.request.post(url=f'{self.gvc_settings.config.cashier_host}deposit/ccInputGuidSubmit.action',
                                 params=params, timeout=20)

    def deposit_mastercard_amount(self, amount: str, auth_token: str, payment_ids: namedtuple, **kwargs):
        """
        Deposit specified amount for specified payments_ids

        :param amount: Amount to deposit
        :param auth_token: User's authorization token
        :param payment_ids: Cashier payments IDs
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        payment_account_id = payment_ids.payment_account_id
        cc_id = payment_ids.cc_id
        payment_method = payment_ids.payment_method
        currency = kwargs.get('currency', 'GBP')

        headers = {
            'auth-code': auth_token
        }

        data = {
            'paymentMethod': payment_method,
            'amountInfo': {
                'nativeCurrency': currency,
                'nativeAmountString': amount
            },
            'bonusInfo': {},
            'paymentAccountInfo': {
                'paymentAccountId': payment_account_id,
                'ccId': cc_id
            }
        }

        params = (
            ('language', 'en'),
            ('source', 'QD')
        )

        url = f'{self.gvc_settings.config.cashier_host}paymentservice/deposit/submit'

        response = self.request.post(url=url, extra_headers=headers, data=json.dumps(data), params=params)
        self._logger.debug(f'*** Got response from depositing: {response}')

        return response

    def _verify_existing_card_response(self, response: dict, **kwargs):
        """
        This method verifies response and generates exception if 'ERROR' appeared in the response
        :param response: Response data
        """
        error_codes = {
            '116': 'Self-set deposit limit exceeded. You have exceeded the daily deposit limit previously set by you.',
            '569': 'Sorry! Your transaction has been declined.',
            'default': 'Sorry! Your transaction has been declined.'
        }

        if response.get('status') == 'FAILURE':
            if kwargs.get('call_from_balance_update'):
                return True
            error_code = response.get('errorResponse').get('errorCode', 'default')
            error_message = error_codes.get(error_code) if error_code in error_codes.keys() else error_codes.get('default')
            raise GVCUserClientException(f'Cannot deposit due error: "{error_message}"')

    def deposit_via_existing_card(self, username: str, amount: str, **kwargs):
        """
        Deposit for specified user via already added card, it there's few cards added, first card will be used

        :param username: User's name
        :param amount: Amount to deposit (22 limit)
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        tokens = self.get_logged_user_api_tokens()
        sso_token = tokens.sso_token

        auth_token = self.get_user_auth_token(username=username,
                                              sso_token=sso_token)

        payment_ids = self.get_deposit_payment_ids(auth_token=auth_token)

        response = self.deposit_mastercard_amount(amount=amount,
                                                  auth_token=auth_token,
                                                  payment_ids=payment_ids,
                                                  **kwargs)

        self._verify_existing_card_response(response=json.loads(response.text))

        return response

    def deposit_via_saved_card(self, username: str, amount: str, card_type: str, **kwargs):
        """
        Deposit for specified user via already added card, it there's few cards added, first card will be used

        :param username: User's name
        :param amount: Amount to deposit (22 limit)
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        tokens = self.get_logged_user_api_tokens()
        sso_token = tokens.sso_token

        auth_token = self.get_user_auth_token(username=username, sso_token=sso_token)
        response = self.fetch_existing_payment_id(auth_code=auth_token, card_type=card_type)
        resp_dict = json.loads(response.text)
        if len(resp_dict['usedPaymentMethods'])>0:
            card_type = resp_dict['usedPaymentMethods'][0]['name']
            payment_ids = resp_dict['usedPaymentMethods'][0]['paymentAccountDetails']['paymentAccountId']

            response1 = self.add_balance_new_flow(amount=amount,
                                                  auth_token=auth_token,
                                                  payment_ids=payment_ids, card_type=card_type,
                                                  **kwargs)
        else:
            card_number = kwargs.get("card_number")
            expiry_month = kwargs.get("expiry_month")
            expiry_year = kwargs.get("expiry_year")
            self.add_new_payment_card_and_deposit(username=username, amount=str(20),
                                                  card_number=card_number,
                                                  card_type=card_type, expiry_month=expiry_month,
                                                  expiry_year=expiry_year,
                                                  cvv='123')

    def fetch_existing_payment_id(self, auth_code, card_type: str, **kwargs):
        """
        Request URL: https://cashier.coral.co.uk/deposit/ccDeleteSubmit.action

        :param kwargs: card_number, card_type, session_key, j_session_id, cc_id
        :return: Response
        """

        cookies = {
            'auth-code': auth_code
        }

        return self.request.get(f'{self.gvc_settings.config.cashier_host}depositservice/deposit/usedOptions',
                                cookies=cookies)

    def add_balance_new_flow(self, amount: str = '5', auth_token: str = None, payment_ids: str = None, card_type = None, **kwargs):
        """
        Deposit specified amount for specified payments_ids

        :param amount: Amount to deposit
        :param auth_token: User's authorization token
        :param payment_ids: Cashier payments IDs
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        currency = kwargs.get('currency', 'GBP')

        headers = {
            'auth-code': auth_token
        }
        card_type = card_type.upper()

        data = {
            "paymentMethod": card_type,
            "amountInfo": {
                "nativeCurrency": currency,
                "nativeAmountString": int(amount) if int(amount) <= 20 else 5
            },
            "bonusInfo": {
                "tncFromBonusService": True,
                "bonusTnCAccepted": None,
                "bonusCode": ""
            },
            "browserInfo": {
                "browserLanguage": "en",
                "browserScreenHeight": 640,
                "browserScreenWidth": 360,
                "browserTimeZone": -330
            },
            "germanAMLChangesEnabled": False,
            "paymentAccountInfo": {
                "paymentAccountId": payment_ids,
                "ccId": None,
                "emailId": "",
                "nameonCard": "MACKENZIE REYES",
                "expiryMonth": "DEC"
            },
            "productPreference": "SPORTSBOOK",
            "worldPaySessionId": "1_9c268532-2143-4cfc-a7a1-0bef36a7d665",
            "worldPaySessionIdStatus": True,
            "pageName": "cc-Input"
        }

        params = (
            ('language', 'en'),
            ('source', 'QD')
        )

        url = f'{self.gvc_settings.config.cashier_host}depositservice/deposit/submit'

        response = self.request.post(url=url, extra_headers=headers, data=json.dumps(data), params=params)
        self._logger.debug(f'*** Got response from depositing: {response}')

        is_failure = self._verify_existing_card_response(response=json.loads(response.text),**kwargs)

        if is_failure:
            return None

        site = lxml.html.fromstring(response.text)

        error_panel = site.xpath('.//div[@class="row"]//*[@class="message-box critical"]')
        if error_panel:
            try:
                error_message = error_panel[0].xpath('.//div[@class="message-text"]//p')[0].text
            except Exception:
                error_message = 'Sorry! Your transaction has been declined.'
            raise GVCUserClientException(f'Cannot deposit due error: "{error_message}"')

        return response

    def create_new_payment_id(self, auth_code, **kwargs):
        """
        Request URL: https://cashier.coral.co.uk/deposit/ccDeleteSubmit.action

        :param kwargs: card_number, card_type, session_key, j_session_id, cc_id
        :return: Response
        """

        cookies = {
            'auth-code': auth_code,
        }

        data_params = {
            'preference': 'VISA',
            'pageName': 'popularOptionPage'
        }

        data = json.dumps(data_params)

        return self.request.post(f'{self.gvc_settings.config.cashier_host}depositservice/deposit/input-details?lang=en',
                                 data=data,
                                 cookies=cookies)

    def add_new_payment_card_and_deposit(self,
                                         username: str,
                                         amount: str,
                                         card_number: str,
                                         card_type: str,
                                         expiry_month: str,
                                         expiry_year: str,
                                         cvv: str,
                                         **kwargs):
        """
        Perform initial deposit in situation when there's no added payment card for specified user

        :param amount: Amount to deposit (22 limit)
        :param card_number: Card number, e.g. 5190023456735555
        :param card_type: Card type, e.g. visa, mastercard
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        tokens = self.get_logged_user_api_tokens()
        sso_token = tokens.sso_token

        auth_token = self.get_user_auth_token(username=username,
                                              sso_token=sso_token)
        response = self.create_new_payment_id(auth_code=auth_token)
        resp_dict = json.loads(response.text)
        payment_ids = resp_dict['paymentInputDetailsInfo']['paymentAccountId']
        card_url_updated = resp_dict['paymentInputDetailsInfo']['token']
        name_on_card = resp_dict['paymentInputDetailsInfo']['nameOnCard']

        resp_dict = self.get_ccguid_for_new_card(card_url=card_url_updated,
                                                 card_number=card_number,
                                                 expiry_month=expiry_month,
                                                 expiry_year=expiry_year,
                                                 cvv=cvv,
                                                 name_on_card=name_on_card)

        response = self.add_balance_new_flow(amount=amount,
                                             auth_token=auth_token,
                                             payment_ids=payment_ids, card_type=card_type,
                                             **kwargs)
        return response

    def add_payment_card_and_deposit(self,
                                     amount: str,
                                     card_number: str,
                                     card_type: str,
                                     expiry_month: str,
                                     expiry_year: str,
                                     cvv: str,
                                     **kwargs):
        """
        Perform initial deposit in situation when there's no added payment card for specified user

        :param amount: Amount to deposit (22 limit)
        :param card_number: Card number, e.g. 5190023456735555
        :param card_type: Card type, e.g. visa, mastercard
        :param expiry_month: Expiry month e.g. 11
        :param expiry_year: Expiry year e.g. 2027
        :param cvv: Card's CVV e.g. 111
        :param kwargs: Additional parameters:
                        - currency - by default 'GBP'
        :return: Request response
        """
        tokens = self.get_logged_user_api_tokens()
        sso_token = tokens.sso_token

        cashier_card_data = self.fetch_cashier_card_data(session_id=sso_token,
                                                         deposit_method=card_type)

        response = self.deposit_via_new_card(amount=amount,
                                             card_type=card_type,
                                             card_number=card_number,
                                             expiry_month=expiry_month,
                                             expiry_year=expiry_year,
                                             cvv=cvv,
                                             cashier_card_data=cashier_card_data,
                                             **kwargs)

        site = lxml.html.fromstring(response.text)

        error_panel = site.xpath('.//div[@class="row"]//*[@class="message-box critical"]')
        if error_panel:
            try:
                error_message = error_panel[0].xpath('.//div[@class="message-text"]//p')[0].text
            except Exception:
                error_message = 'Sorry! Your transaction has been declined.'
            raise GVCUserClientException(f'Cannot deposit due error: "{error_message}"')

        return response

    def get_gambling_controls_data(self, username, password):
        """
        Method gets Gambling Controls data

        :param username: User's name
        :param password: User's password
        :return: dict with Gambling Controls data
        """
        self.login(username=username, password=password)
        url = f'{self.gvc_settings.config.mobileportal}GamblingControls/GetInitData'

        response = self.request.get(url=url)
        resp_dict = response.json()
        return resp_dict

    def get_deposit_limits_data(self, username, password):
        """
        Method gets Deposit Limits data

        :param username: User's name
        :param password: User's password
        :return: dict with Deposit Limits data
        """
        self.login(username=username, password=password)
        url = f'{self.gvc_settings.config.mobileportal}depositLimitsPage/getInitData'

        response = self.request.get(url=url)
        resp_dict = response.json()
        return resp_dict

    def get_account_closure_data(self, username, password):
        """
        Method gets Account Closure options

        :param username: User's name
        :param password: User's password
        :return: dict with Account Closure options
        """
        self.login(username=username, password=password)
        url = f'{self.gvc_settings.config.mobileportal}AccountClosure/GetInitData'

        response = self.request.get(url=url)
        resp_dict = response.json()
        return resp_dict

    def get_service_closure_data(self, username, password):
        """
        Method gets Service Closure data

        :param username: User's name
        :param password: User's password
        :return: dict with Service Closure data
        """
        self.login(username=username, password=password)
        url = f'{self.gvc_settings.config.mobileportal}serviceClosure/GetInitData'

        response = self.request.get(url=url)
        resp_dict = response.json()
        return resp_dict

    def get_communication_preferences_data(self, username, password):
        """
        Method gets Communication Preferences data

        :param username: User's name
        :param password: User's password
        :return: dict with Communication Preferences data
        """
        self.login(username=username, password=password)
        url = f'{self.gvc_settings.config.mobileportal}communication/GetInitData'

        response = self.request.get(url=url)
        resp_dict = response.json()
        return resp_dict

    def create_inshop_user_card_generation(self):
        """
        Method creates the In-Shop User Card Number
        """
        user_name = self._generate_username()
        email = self._generate_email(user_name)
        password = 1234
        user_details = {'user_name': user_name, 'email': email, 'card_pin': password}
        firstname = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        casino_name = "coraltst2" if self.brand == "bma" else "ladbrokesvegas"
        in_shop_user_creation_url = f'{self.gvc_settings.config.in_shop_user_card_generation}set-player-info'
        user_creation_data = '''<?xml version="1.0" encoding="UTF-8"?>
                                <setPlayerInfoRequest
                                xmlns="http://www.playtech.com/services/player-management">
                                <changeTimestamp>2019-06-12 08:50:40.264</changeTimestamp>
                                <behaviourType>Create</behaviourType>
                                <playerDataMap>
                                <username>''' + user_name + '''</username>
                                <password>Qwerty19</password>
                                <address>Dunorlan House, Dunorlan Park Pembury Road</address>
                                <birthDate>1988-01-01</birthDate>
                                <cellPhone>+4407832432626</cellPhone>
                                <city>Tunbridge Wells</city>
                                <countryCode>GB</countryCode>
                                <currency>GBP</currency>
                                <email>''' + email + '''</email>
                                <firstName>''' + firstname + '''</firstName>
                                <lastName>tom</lastName>
                                <phone>+4401892530899</phone>
                                <title>mr</title>
                                <custom19>true</custom19>
                                <zip>TN2 3QA</zip>
                                <accountBusinessPhase>in-shop</accountBusinessPhase>
                                <wantMail>1</wantMail>
                                <signupVenue>1606</signupVenue>
                                <remoteIp>52.56.242.70</remoteIp>
                                <clientType>retail</clientType>
                                <signupClientPlatform>retailotc</signupClientPlatform>
                                <signupDeviceType>PC</signupDeviceType>
                                </playerDataMap>
                                </setPlayerInfoRequest>'''
        user_creation_headers = {'Content-Type': 'application/xml',
                                 'x-casinoname': casino_name}
        user_creation_response = self.request.post(url=in_shop_user_creation_url, extra_headers=user_creation_headers,
                                                   data=user_creation_data)
        if (user_creation_response.json()["username"]) != user_name:
            raise GVCUserClientException("User Creation Failed")
        user_token_count = 16 if self.brand == "bma" else 12
        user_token = ''.join(random.choice(string.digits) for _ in range(user_token_count))
        user_details.update({"card_number": user_token})
        inshop_user_cardnumber_generation_url = f'{self.gvc_settings.config.in_shop_user_card_generation}create-idtoken'
        card_generation_data = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                                    <ns5:createIdTokenRequest xmlns:ns5="http://www.playtech.com/services/player-management" xmlns:ns2="http://www.playtech.com/services/common">
                                    <ns5:username>''' + user_name + '''</ns5:username>
                                    <ns5:token>
                                    <ns5:tokenCode>''' + user_token + '''</ns5:tokenCode>
                                    <ns5:printedTokenCode>''' + user_token + '''</ns5:printedTokenCode>
                                    <ns5:pin>1234</ns5:pin>
                                    <ns5:registrationTime>2018-12-18 07:34:57.630</ns5:registrationTime>
                                    <ns5:registrationDevice>device.identifier</ns5:registrationDevice>
                                    <ns5:registrationVenue>venue.identifier</ns5:registrationVenue>
                                    <ns5:status>open</ns5:status>
                                    <ns5:tokenType>RFID</ns5:tokenType>
                                    </ns5:token>
                                    </ns5:createIdTokenRequest>'''
        card_number_generation_response = self.request.post(url=inshop_user_cardnumber_generation_url,
                                                            extra_headers=user_creation_headers,
                                                            data=card_generation_data)
        if card_number_generation_response.status_code != 200:
            raise GVCUserClientException("User Card Creation Failed")
        return user_details


if __name__ == '__main__':
    v = GVCUserClient()
