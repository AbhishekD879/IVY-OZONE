import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_account
@pytest.mark.bet_placement
@pytest.mark.quick_bet
@pytest.mark.betslip
@pytest.mark.bpp
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.medium
@vtest
class Test_C26524536_Verify_there_are_no_duplicated_BPP_auth_requests(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C26524536
    NAME: Verify there are no duplicated BPP auth requests
    DESCRIPTION: This test case verifies there are no multiple BPP auth requests on My Bets/Cashout, Betslip, QuickBet, and Homepage (or any other page)
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has at least 1 stake placed with cashout available
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    cookie_name = 'OX.USER'
    cookie_parameter = 'bppToken'
    number_of_auth_requests = 1

    def get_number_of_auth_requests(self) -> int:
        """
        This method returns number of authentication requests
        :return: number of authentication requests in performance log
        """
        log = self.device.get_performance_log(preserve=False)
        expected_url = f'{tests.settings.bpp}auth/user'
        expected_method = 'POST'
        entries = []
        for entry in log:
            for entry_field in entry:
                for entry_type, entry_value in entry_field.items():
                    if entry_type == 'message':
                        params = entry_value.get('message', {}).get('params', {})
                        url = params.get('request', {}).get('url', '')
                        method = params.get('request', {}).get('method', '')
                        if url == expected_url and method == expected_method:
                            entries.append(entry)
        return len(entries)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find/Create events
        DESCRIPTION: Login with user
        DESCRIPTION: Place a bet with cashout available
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            self.__class__.eventID = event.get('event').get('id')
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.info(f'*** Found Football event with id "{self.eventID}" with selection ids: "{self.selection_ids}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            self.__class__.eventID = event.event_id
            self.__class__.selection_ids = event.selection_ids
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
            self._logger.info(f'*** Created Football event with selection ids: "{self.selection_ids}"')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)

        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_open_devtools_application_local_storage_and_modify_bpptoken_value_in_ox_user(self):
        """
        DESCRIPTION: Open devtools > Application > Local Storage and modify bpp.Token value in OX.USER
        EXPECTED: Token is modified
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value before change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

        cookie_value[self.cookie_parameter] = '123'
        self.device.set_local_storage_cookies(ls_cookies_dict={self.cookie_name: cookie_value})

        cookie_value = self.get_local_storage_cookie_value(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value after change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

    def test_002_refresh_page_open_devtools_network_xhr_and_verify_auth_requests(self):
        """
        DESCRIPTION: Refresh page
        DESCRIPTION: Open devtools > Network > XHR and verify auth requests (ex: Request URL: https://bpp.ladbrokes.com/Proxy/auth/user)
        EXPECTED: There is only 1 auth request
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_logged_in()

        auth_requests = self.get_number_of_auth_requests()
        self.assertEqual(auth_requests, self.number_of_auth_requests,
                         msg=f'Actual number of authentication requests: "{auth_requests}" '
                             f'is not as expected: "{self.number_of_auth_requests}"')

    def test_003_stay_logged_in_and_navigate_to_my_bets_open_bets(self):
        """
        DESCRIPTION: Stay logged in and navigate to My Bets > Open Bets
        """
        self.site.wait_logged_in()
        self.site.open_my_bets_open_bets()

    def test_004_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        EXPECTED: There is only 1 auth request
        """
        self.test_001_open_devtools_application_local_storage_and_modify_bpptoken_value_in_ox_user()
        self.test_002_refresh_page_open_devtools_network_xhr_and_verify_auth_requests()

    def test_005_logout_and_add_selection_to_quickbet_click_login_and_place_bet(self):
        """
        DESCRIPTION: Logout and add selection to QuickBet. Click Login and place bet
        EXPECTED: Login pop up displayed
        """
        if self.device_type != 'desktop':
            self.site.logout()
            self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
            self.navigate_to_edp(event_id=self.eventID)

            self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            self.assertTrue(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=20),
                            msg='Login dialog is not present on page')

    def test_006_login_to_app_open_devtools_network_xhr_and_verify_auth_requests(self):
        """
        DESCRIPTION: Login to app
        DESCRIPTION: Open devtools > Network > XHR and verify auth requests (ex: Request URL: https://bpp.ladbrokes.com/Proxy/auth/user)
        EXPECTED: There is only 1 auth request
        """
        if self.device_type != 'desktop':
            try:
                self.site.login(username=self.username)
            except Exception as e:
                self._logger.warning(e)
                self.site.wait_content_state_changed()
            auth_requests = self.get_number_of_auth_requests()
            self.assertEqual(auth_requests, self.number_of_auth_requests,
                             msg=f'Actual number of authentication requests: "{auth_requests}" '
                                 f'is not as expected: "{self.number_of_auth_requests}"')
