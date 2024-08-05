import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.bpp_config import BPPConfig
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # This functionality is no longer applicable from release 108
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.critical
# @pytest.mark.betslip
# @pytest.mark.cash_out
# @pytest.mark.bet_placement
# @pytest.mark.bpp
# @pytest.mark.desktop
# @pytest.mark.login
# @pytest.mark.safari
@pytest.mark.na
@vtest
class Test_C3009204_Verify_that_user_is_logged_in_and_able_to_place_bets_after_BPP_token_is_updated(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C3009204
    NAME: Verify that user is logged in and able to place bets after BPP token is updated
    DESCRIPTION: This test case verifies that user is logged in and able to place bets/cashout after BPP token is updated
    """
    keep_browser_open = True
    bpp_config = BPPConfig()
    cookie_name = 'OX.USER'
    cookie_parameter = 'bppToken'
    status_code = 204

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Application is launched
        PRECONDITIONS: 2. User is logged in to application
        PRECONDITIONS: 3. Trigger situation when BPP token is wrong or expired:
        PRECONDITIONS: * Open Postman
        PRECONDITIONS: * Send DELETE request to correct BPP from **user** request > 'Preview' with actual **Headers** for request:
        PRECONDITIONS: https://{domain}/Proxy/auth/invalidateSession
        PRECONDITIONS: **token** key - with current BPP token value
        PRECONDITIONS: **username** key - with currently logged in user's login
        PRECONDITIONS: where **{domain}** may be
        PRECONDITIONS: * https://bpp-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com - Ladbrokes TST2
        PRECONDITIONS: * https://hl-bpp.ladbrokes.com - Ladbrokes HL
        PRECONDITIONS: * https://bp-hl.coral.co.uk - Coral BETA
        PRECONDITIONS: **etc.**
        PRECONDITIONS: e.g. ![](index.php?/attachments/get/28190)
        PRECONDITIONS: Request returns **204 No Content** status code
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            self.__class__.event_name = event['event']['name']
            outcomes = event['event']['children'][0]['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            name_pattern = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
            event_time_local = self.convert_time_to_local(date_time_str=event.event_date_time)
            self.__class__.event_name = f'{name_pattern} {event_time_local}'
            self.__class__.selection_ids = event.selection_ids
        self._logger.info(f'*** Found/created Horse racing event "{self.event_name}" with selections "{self.selection_ids}"')

        # logging and delete bpp token
        username = tests.settings.betplacement_user
        self.site.login(username=username, async_close_dialogs=False)
        bpp_token = self.get_local_storage_cookie_value_as_dict(self.cookie_name).get(self.cookie_parameter)
        self.assertTrue(bpp_token, msg='BPP token is not received')

        resp = self.bpp_config.delete_bpp_token(bpp_user_token=bpp_token, username=username)
        self.assertEqual(resp.status_code, self.status_code, msg=f'Request status code "{resp.status_code}" '
                                                                 f'is not equal to expected {self.status_code}')

    def test_001_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in_after_passing_preconditions(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in (after passing Preconditions)
        EXPECTED: * User is still logged in to application
        EXPECTED: * User has BPP token value assigned (Check in **OX.USER** parameter in Dev Tools -> Application -> Local Storage)
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in to application')
        bpp_token = self.get_local_storage_cookie_value_as_dict(self.cookie_name).get(self.cookie_parameter)
        self.assertTrue(bpp_token, msg='BPP token is not received')

    def test_002_add_selection_to_the_betslip_where_cash_out_is_available_and_place_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip (where cash out is available) and place bet
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_003__go_to_open_bets___cash_out_section_make_full_partial_cash_out(self):
        """
        DESCRIPTION: * Go to Open Bets - Cash out section.
        DESCRIPTION: * Make full/partial Cash out
        EXPECTED: Cash out process is successfully done
        """
        self.site.open_my_bets_cashout()

        self.__class__.bet_name, self.__class__.bet = \
            self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                  event_names=self.event_name, number_of_bets=1,
                                                                  timeout=45)
        self.bet.scroll_to()
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not present')
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

    def test_004_in_dev_tools___application___local_storage_select_app_url_for_oxuser_parameter_change_bpptoken_value_and_save_changesin_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In Dev Tools -> Application -> Local Storage select app url
        DESCRIPTION: For OX.USER parameter change bppToken: value and save changes
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: * User is still logged in to application
        EXPECTED: * User has same BPP token value assigned as before manual value change (could be checked in **OX.USER** parameter in Dev Tools -> Application -> Local Storage)
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value before change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

        cookie_value[self.cookie_parameter] = '123'
        self.device.set_local_storage_cookies(ls_cookies_dict={self.cookie_name: cookie_value})

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_logged_in()
        result = wait_for_result(
            lambda: self.get_local_storage_cookie_value_as_dict(self.cookie_name).get(self.cookie_parameter),
            name='BPP token to be received',
            timeout=10)

        self.assertTrue(result, msg='BPP token is not received')

    def test_005_add_selection_to_the_betslip_where_cash_out_is_available_and_place_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip (where cash out is available) and place bet
        EXPECTED: Bet is placed successfully
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_006__go_to_open_bets___cash_out_section_make_full_partial_cash_out(self):
        """
        DESCRIPTION: * Go to Open Bets - Cash out section.
        DESCRIPTION: * Make full/partial Cash out
        EXPECTED: Cash out process is successfully done
        """
        self.site.open_my_bets_cashout()

        self.__class__.bet_name, self.__class__.bet = \
            self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                  event_names=self.event_name, number_of_bets=1,
                                                                  timeout=45)
        self.bet.scroll_to()
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not present')

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')
