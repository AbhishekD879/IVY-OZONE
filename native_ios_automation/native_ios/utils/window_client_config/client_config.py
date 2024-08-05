import json

from native_ios.pages.shared import get_device_properties
from native_ios.utils import mixins
from native_ios.utils.exceptions.voltron_exception import VoltronException


class WindowClientConfig(mixins.LoggingMixin):

    def __init__(self, config, brand, *args, **kwargs):
        super(WindowClientConfig, self).__init__(*args, **kwargs)
        self.config = config
        self.brand = brand

    def get_gvc_config_item(self, key_title: str, value_title: str = None, context: dict = None) -> dict:
        """
        Method used to get GVC config from window.clientConfig
        :param key_title: Title of required key object in clientConfig
        :param value_title: Value of required object in clientConfig (if known)
        :param context: If specified - searching data will be provided in this dict instead of whole config
        :return: nested dict where required key is located
        Usages:
        >>> self.get_gvc_config_item(key_title='name', value_title='cashiernew')
        Or:
        >>> self.get_gvc_config_item(key_title='CoralCashbackText')
        """

        def find_nested_dict_item(dictionary):
            """
            Recursively checking for nested dict object presence by key/value
            """
            dict_value = dictionary.get(key_title)
            if value_title:
                if dict_value == value_title:
                    return dictionary
            else:
                if dict_value:
                    return dictionary
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    result = find_nested_dict_item(dictionary=value)
                    if result:
                        return result
                elif isinstance(value, list):
                    for list_item in value:
                        if isinstance(list_item, dict):
                            result = find_nested_dict_item(dictionary=list_item)
                            if result:
                                return result
        dict_to_search = context if context else self.config
        item_found = find_nested_dict_item(dictionary=dict_to_search)
        if not item_found:
            raise VoltronException(f'Item with "{key_title}/{value_title}" key/value not found')
        self._logger.debug(f'*** Found config: {json.dumps(item_found, indent=2)}')
        return item_found

    def get_gvc_config_item_text(self, **kwargs):
        item = self.get_gvc_config_item(**kwargs)
        text = item.get('text')
        return self.__convert_right_menu_name_for_brand(text)

    def __convert_right_menu_name_for_brand(self, text: str) -> str:
        """
        Method converts name from User's Right Menu to the .upper/.title() depends on the brand:
            - Ladbrokes both mobile/desktop - title case always
            - Coral both mobile/desktop - upper case always
        :param text: Specified text to convert
        :return: Converted text
        """
        return text.upper() if self.brand == 'bma' else text

    @property
    def cookie_enabled(self) -> bool:
        """
        Method to get status of cookie displaying
        """
        cookies = self.config.get('vnCookieConsent')
        cookies_status = cookies.get('condition')
        return False if cookies_status == 'false' else True

    # =================== RIGHT MENU ITEMS ===================
    # dict path: window.clientConfig => vnMenu
    @property
    def cashier_menu_title(self) -> str:
        """
        Method to get GVC Cashier Menu title
        """
        cashier_config = self.get_gvc_config_item(key_title='name', value_title='cashiernew')
        cashier_title = cashier_config.get('text')
        if not cashier_title:
            raise VoltronException('Cannot get Cashier Menu title')
        return self.__convert_right_menu_name_for_brand(cashier_title)

    @property
    def deposit_menu_title(self) -> str:
        """
        Method to get GVC Deposit Menu title
        """
        deposit_config = self.get_gvc_config_item(key_title='name', value_title='deposit')
        deposit_title = deposit_config.get('text')
        if not deposit_title:
            raise VoltronException('Cannot get Deposit Menu title')
        return self.__convert_right_menu_name_for_brand(deposit_title)

    @property
    def offers_menu_title(self) -> str:
        """
        Method to get GVC Offers Menu title
        """
        offers = self.get_gvc_config_item(key_title='menuRoute', value_title='menu/offers')
        offers_title = offers.get('text')
        if not offers_title:
            raise VoltronException('Cannot get Offers Menu title')
        return self.__convert_right_menu_name_for_brand(offers_title)

    @property
    def sports_freebets_menu_title(self) -> str:
        """
        Method to get GVC Sports Freebets Menu title
        """
        sports_freebets = self.get_gvc_config_item(key_title='name', value_title='sportsfreebets')
        sports_freebets_title = sports_freebets.get('text')
        if not sports_freebets_title:
            raise VoltronException('Cannot get Sports Freebets Menu title')
        return self.__convert_right_menu_name_for_brand(sports_freebets_title)

    @property
    def settings_menu_title(self) -> str:
        """
        Method to get GVC Offers Menu title
        """
        settings = self.get_gvc_config_item(key_title='menuRoute', value_title='menu/settings')
        settings_title = settings.get('text')
        if not settings_title:
            raise VoltronException('Cannot get Settings Menu title')
        return self.__convert_right_menu_name_for_brand(settings_title)

    @property
    def betting_settings_menu_title(self) -> str:
        """
        Method to get GVC Offers Menu title
        """
        betting_settings = self.get_gvc_config_item(key_title='name', value_title='bettingsettings')
        betting_settings_title = betting_settings.get('text')
        if not betting_settings_title:
            raise VoltronException('Cannot get Betting Settings Menu title')
        return self.__convert_right_menu_name_for_brand(betting_settings_title)

    @property
    def marketing_preferences_menu_title(self) -> str:
        """
        Method to get GVC Offers Menu title
        """
        marketing_preferences = self.get_gvc_config_item(key_title='name', value_title='marketingpreferences')
        marketing_preferences_title = marketing_preferences.get('text')
        if not marketing_preferences_title:
            raise VoltronException('Cannot get Marketing Preferences Menu title')
        return self.__convert_right_menu_name_for_brand(marketing_preferences_title)

    @property
    def communication_preferences_menu_title(self) -> str:
        """
        Method to get GVC Offers Menu title
        """
        communication_preferences = self.get_gvc_config_item(key_title='name', value_title='communicationpreferences')
        communication_preferences_title = communication_preferences.get('text')
        if not communication_preferences_title:
            raise VoltronException('Cannot get Communication Preferences Menu title')
        return self.__convert_right_menu_name_for_brand(communication_preferences_title)

    @property
    def change_password_menu_title(self) -> str:
        """
        Method to get GVC 'Change Password' Menu title
        """
        change_password = self.get_gvc_config_item(key_title='name', value_title='changepassword')
        change_password_title = change_password.get('text')
        if not change_password_title:
            raise VoltronException('Cannot get Change Password Menu title')
        return self.__convert_right_menu_name_for_brand(change_password_title)

    @property
    def gambling_controls_title(self) -> str:
        """
        Method to get Gambling controls Menu title
        """
        gambling_controls = self.get_gvc_config_item(key_title='name', value_title='gamblingcontrols')
        gambling_controls_title = gambling_controls.get('text')
        if not gambling_controls_title:
            raise VoltronException('Cannot get Gambling controls Menu title')
        return self.__convert_right_menu_name_for_brand(gambling_controls_title)

    @property
    def betting_settings_title(self) -> str:
        """
        Method to get Betting Settings Menu title
        """
        betting_settings = self.get_gvc_config_item(key_title='name', value_title='bettingsettings')
        betting_settings_title = betting_settings.get('text')
        if not betting_settings_title:
            raise VoltronException('Cannot get Betting Settings Menu title')
        return self.__convert_right_menu_name_for_brand(betting_settings_title)

    @property
    def history_title(self) -> str:
        """
        Method to get Gambling controls Menu title
        """
        history = self.get_gvc_config_item(key_title='name', value_title='history')
        history_title = history.get('text')
        if not history_title:
            raise VoltronException('Cannot get History Menu title')
        return self.__convert_right_menu_name_for_brand(history_title)

    @property
    def betting_history_title(self) -> str:
        """
        Method to get Gambling controls Menu title
        """
        betting_history = self.get_gvc_config_item(key_title='name', value_title='betting')
        betting_history_title = betting_history.get('text')
        if not betting_history_title:
            raise VoltronException('Cannot get Betting History Menu title')
        return self.__convert_right_menu_name_for_brand(betting_history_title)

    @property
    def odds_boost_menu_title(self) -> str:
        """
        Method to get Betting Settings Menu title
        """
        odds_boost = self.get_gvc_config_item(key_title='name', value_title='oddsboost')
        odds_boost_title = odds_boost.get('text')
        if not odds_boost_title:
            raise VoltronException('Cannot get Odds Boost Menu title')
        return self.__convert_right_menu_name_for_brand(odds_boost_title)

    @property
    def connect_card_empty_credentials_error(self) -> str:
        """
        Method to get connect card empty credentials error text
        """
        empty_credentials = self.get_gvc_config_item(key_title='EmptyCredentials')
        error_text = empty_credentials.get('EmptyCredentials')
        if not error_text:
            raise VoltronException('Cannot get connect card empty credentials error text')
        return error_text

    # =================== DESKTOP HEADER ITEMS ===================
    # dict path: window.clientConfig => vnResponsiveHeader
    @property
    def gaming_header_item_name(self) -> str:
        """
        Method to get GVC desktop top header 'Gaming' name
        """
        gaming_item = self.get_gvc_config_item(key_title='name', value_title='games')
        gaming_name = gaming_item.get('text')
        if not gaming_name:
            raise VoltronException('Cannot get Gaming item name')
        return gaming_name.upper()  # both coral/ladbrokes have header items with upper case

    # =================== MOBILE PORTAL SETTINGS ===================
    # dict path: window.clientConfig => lhNavigationLayout
    def __convert_mobile_portal_setting_name_for_brand(self, text: str) -> str:
        """
        Example of link - https://beta-sports.ladbrokes.com/en/mobileportal/changepassword
        Method converts mobile settings to the .upper/.title() depends on the brand:
            - Coral mobile - upper case always
            - Ladbrokes both mobile/desktop and Coral desktop - title case always
        :param text: Specified text to convert
        :return: Converted text
        """
        if self.brand == 'bma' and get_device_properties()['type'] == 'mobile':
            return text.upper()
        else:
            return text

    @property
    def mobile_portal_communication_setting(self) -> str:
        """
        Method to get GVC Mobile Portal Communication Preferences settings
        """
        marketing_preferences = self.get_gvc_config_item(key_title='name', value_title='communication')
        marketing_preferences_title = marketing_preferences.get('text')
        if not marketing_preferences_title:
            raise VoltronException('Cannot get GVC Mobile Portal Communication Preferences settings title')
        return self.__convert_mobile_portal_setting_name_for_brand(marketing_preferences_title)

    @property
    def mobile_portal_transaction_history(self) -> str:
        """
        Method to get GVC Mobile Portal Transaction History settings
        """
        marketing_preferences = self.get_gvc_config_item(key_title='name', value_title='transactions')
        marketing_preferences_title = marketing_preferences.get('text')
        if not marketing_preferences_title:
            raise VoltronException('Cannot get GVC Mobile Portal Transaction History settings title')
        return self.__convert_mobile_portal_setting_name_for_brand(marketing_preferences_title)

    @property
    def mobile_portal_gambling_controls(self) -> str:
        """
        Method to get GVC Mobile Portal Gambling Controls settings
        """
        marketing_preferences = self.get_gvc_config_item(key_title='name', value_title='gamblingcontrols')
        marketing_preferences_title = marketing_preferences.get('text')
        if not marketing_preferences_title:
            raise VoltronException('Cannot get GVC Mobile Portal Gambling Controls settings title')
        return self.__convert_mobile_portal_setting_name_for_brand(marketing_preferences_title)

    @property
    def mobile_portal_spending_controls(self) -> str:
        """
        Method to get GVC Mobile Portal Spending Controls settings (Deposit Limits etc)
        """
        spending_controls = self.get_gvc_config_item(key_title='name', value_title='spendingcontrols')
        spending_controls_title = spending_controls.get('text')
        if not spending_controls_title:
            raise VoltronException('Cannot get GVC Mobile Portal Spending Controls settings title')
        return spending_controls_title
