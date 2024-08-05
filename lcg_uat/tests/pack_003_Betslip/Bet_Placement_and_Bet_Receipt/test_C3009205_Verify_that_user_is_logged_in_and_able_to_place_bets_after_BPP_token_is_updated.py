import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.cash_out
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C3009205_Verify_that_user_is_logged_in_and_able_to_place_bets_after_BPP_token_is_updated(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C3009205
    NAME: Verify that user is logged in and able to place bets after BPP token is updated
    DESCRIPTION: This test case verifies that user is logged in and able to place bets after BPP token is updated
    PRECONDITIONS: User is logged in to application and has placed bets with available cash out
    """
    keep_browser_open = True
    cookie_name = 'OX.USER'
    cookie_parameter = 'bppToken'

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active event
        DESCRIPTION: Log in to application and place bets with available cash out
        EXPECTED: User is logged in to application and has placed bets with available cash out
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=1)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])

            outcomes = event['event']['children'][0]['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            self._logger.info(f'*** Found event "{self.event_name}" with selections: {self.selection_ids}')
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self._logger.info(f'*** Created Horse racing event "{event}"')

            name_pattern = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
            event_time_local = self.convert_time_to_local(date_time_str=event.event_date_time)

            self.__class__.event_name = f'{name_pattern} {event_time_local}'
            self.__class__.selection_ids = event.selection_ids

        username = tests.settings.betplacement_user
        self.site.login(username=username)

    def test_001_in_dev_tools_application_local_storage_select_app_url(self):
        """
        DESCRIPTION: In Dev Tools -> Application -> Local Storage select app url
        DESCRIPTION: For OX.USER parameter change "bppToken" value and save changes
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value before change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

        cookie_value[self.cookie_parameter] = '123'
        self.device.set_local_storage_cookies(ls_cookies_dict={self.cookie_name: cookie_value})

        cookie_value = self.get_local_storage_cookie_value(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value after change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

    def test_002_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: User is still logged in to application
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_logged_in()
        self.site.close_all_dialogs(timeout=10)

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added and displayed in the Betslip
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_004_place_bet_for_the_selection(self):
        """
        DESCRIPTION: Place bet for the selection
        EXPECTED: Bet is placed successfully
        """
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_005_go_to_open_bets_cashout_section_and_make_full_or_partial_cashout(self):
        """
        DESCRIPTION: Go to Open Bets -> Cashout section
        DESCRIPTION: Make full/partial cashout
        EXPECTED: Cashout process is successfully done
        """
        self.site.open_my_bets_cashout()

        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
            event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.bet.scroll_to()
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not present')

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')
