import re
import time
from datetime import datetime

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.pages.shared import set_driver
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


class BaseUserAccountTest(Common):
    currency = 'GBP'

    # https://jira.egalacoral.com/browse/VANO-1705
    currency_symbols = {
        'GBP': '£',
        'USD': tests.settings.usd_sign,
        'EUR': '€',
    }

    @property
    def vip_users(self):
        vip_users = {
            'gold_user': tests.settings.gold_user_vip_level_13,
            'silver_user': tests.settings.silver_user_vip_level_12,
            'bronze_user': tests.settings.bronze_user_vip_level_11,
            'platinum_user': tests.settings.platinum_user_vip_level_14
        }
        return vip_users

    def logout(self, site):
        site.logout()
        result = site.wait_logged_out(timeout=5)
        self.assertTrue(result, msg='User is not logged out')

    def create_new_browser_instance(self):
        set_driver(None)
        self.__class__._device = None
        self._logger.info('*** Creating new instance of the browser')
        self.device.open_url(url=tests.HOSTNAME)
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                from voltron.pages.ladbrokes.ladbrokes_mobile_site import LadbrokesMobileSite
                site2 = LadbrokesMobileSite()
            else:
                from voltron.pages.ladbrokes.ladbrokes_desktop_site import LadbrokesDesktopSite
                site2 = LadbrokesDesktopSite()
        else:
            if self.device_type == 'mobile':
                from voltron.pages.coral.mobile_site import MobileSite
                site2 = MobileSite()
            else:
                from voltron.pages.coral.desktop_site import DesktopSite
                site2 = DesktopSite()
        self._logger.info(f'*** Recognized {site2.__class__.__name__} for "{self.brand}" brand and "{self.device_type}" device')
        site2.wait_splash_to_hide()
        return site2

    def set_driver(self, driver, device):
        """
        For tests where two browser instances are invoked to set default driver back for Oxygen site
        """
        set_driver(driver)
        self.__class__._device = device
        self.setUpSite()

    def logout_in_new_tab(self):
        """
        This method opens new tab on the same browser instance, clicks 'Logout' and navigates back to first tab
        """
        self.device.open_new_tab()
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('HomePage')
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')
        self.site.logout()
        self.site.wait_content_state('HomePage')
        time.sleep(1)
        self.device.close_current_tab()
        self.device.open_tab(tab_index=0)

    def verify_logged_out_state(self, timeout=90):
        """
        For tests that are verifying app behaviour after logout in separate tab
        Means that user's session is over on the server.
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=timeout)
        self.assertTrue(dialog, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog is not shown')
        # actual_error = dialog.error_message
        # self.assertEqual(actual_error, vec.gvc.SESSION_EXPIRED_DIALOG_TITLE,
        #                  msg=f'Actual error "{actual_error}"!= Expected "{vec.gvc.SESSION_EXPIRED_DIALOG_TITLE}"')
        dialog.close_dialog()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')

    def get_iapiconf_parameter_value(self, parameter):
        iapiConf = self.site.get_iapiconf
        self.assertTrue(parameter in iapiConf.keys(), msg='"%s" key is not find in "%s"' % (parameter, '", "'.join(iapiConf.keys())))
        return iapiConf[parameter]

    def verify_freebet_details_page(self):
        date_now = datetime.utcnow()
        freebet_page = self.site.freebet_details
        self.assertTrue(freebet_page.title, msg='Freebet title is not present')
        if not freebet_page.used_by:
            self._logger.warning('Freebet used by date is not present')
        else:
            self.assertTrue(freebet_page.used_by, msg='Freebet used by date is not present')
            self.assertTrue(date_now <= freebet_page.used_by, msg='Current offer is expired')
        if not freebet_page.expires:
            self._logger.warning('Freebet expiration date is not present')
        else:
            self.assertIn(' day', freebet_page.expires, msg='Expires date is not correct: "day" word is not found')

        self.assertTrue(freebet_page.value, msg='Freebet value is not present')
        self.assertTrue(freebet_page.bet_now, msg='Bet Now button is not present')

    def add_card_and_deposit(self,
                             username: str,
                             amount: str,
                             card_number: str = tests.settings.visa_card,
                             expiry_month='',
                             expiry_year='',
                             cvv=None,
                             **kwargs):
        """
        Make initial deposit for specified user with using specified card

        :param username: User's name to deposit
        :param amount: Amount to deposit (limit is 22)
        :param card_number: Card's number
        :param expiry_month: Card's expiry month
        :param expiry_year: Card's expiry year
        :param cvv: Card's CVV
        """
        verified_card_type = None

        now = datetime.now()
        if not expiry_month:
            expiry_month = now.month
        if not expiry_year:
            shifted_year = str(now.year + 5)
            expiry_year = shifted_year

        card_type_regex = {
            "mastercard": '^5',
            "visa": '^4'
        }
        for card_type, regex in card_type_regex.items():
            if re.match(regex, str(card_number)):
                verified_card_type = card_type
                break
        if not verified_card_type:
            raise VoltronException(f'Card type of "{card_number}" card number was not defined')
        if verified_card_type == 'mastercard':
            cvv = tests.settings.master_card_cvv
        elif verified_card_type == 'visa':
            cvv = tests.settings.visa_card_cvv

        self.gvc_wallet_user_client.login(username=username)
        self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=amount,
                                                                 card_number=card_number,
                                                                 card_type=verified_card_type,
                                                                 expiry_month=expiry_month,
                                                                 expiry_year=expiry_year,
                                                                 cvv=cvv,
                                                                 **kwargs)

    def deposit_with_existing_card_via_cashier(self, username: str, amount: float, card_number=None, **kwargs):
        """
        Make deposit using existing card

        :param username: User's name to deposit
        :param amount: Amount to deposit (no limits)
        :param card_number: Card to deposit in case quick deposit is disabled
        """
        limit = 20
        self.gvc_wallet_user_client.login(username=username)
        qd_enabled = self.gvc_wallet_user_client.quick_deposit_enabled()

        if amount > limit:
            deposit_count = int(amount // limit)
            for _ in range(deposit_count):
                if qd_enabled:
                    self.gvc_wallet_user_client.deposit_via_existing_card(username=username, amount=limit, **kwargs)
                else:
                    self.add_card_and_deposit(username=username, amount=str(limit), card_number=card_number)
                    time.sleep(5)
            amount -= deposit_count * limit
        if amount:
            if qd_enabled:
                self.gvc_wallet_user_client.deposit_via_existing_card(username=username, amount=amount, **kwargs)
            else:
                self.add_card_and_deposit(username=username, amount=str(amount), card_number=card_number)

    def check_my_bets_counter_enabled_in_cms(self):
        bets_counter = self.get_initial_data_system_configuration().get('BetsCounter')
        if not bets_counter:
            bets_counter = self.cms_config.get_system_configuration_item('BetsCounter')
        if not bets_counter.get('enabled'):
            raise CmsClientException('Bets Counter is disabled in CMS')

        cms_footer_menus = self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
        if not cms_footer_menus:
            raise CmsClientException('Footer Menu item not found in System Configuration')

        my_bets_menu = next((menu for menu in cms_footer_menus if 'open-bets' in menu.get('targetUri')), None)
        if not my_bets_menu:
            raise CmsClientException('My Bets menu not enabled in Footer Menu CMS')

    def get_my_bets_from_footer(self):
        menu_items = self.site.navigation_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Footer menu items are not found')

        my_bets = menu_items.get(vec.sb.MY_BETS_FOOTER_ITEM)
        self.assertTrue(my_bets, msg=f'"{vec.sb.MY_BETS_FOOTER_ITEM}" is not found in {menu_items.keys()}')
        return my_bets

    def get_my_bets_counter_value_from_footer(self):
        return self.get_my_bets_from_footer().indicator
