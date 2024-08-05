import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.prod # Need to settle event
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C16408293_Verify_My_Bets_counter_updating_after_navigation_to_My_Bets_page(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16408293
    NAME: Verify My Bets counter updating after navigation to My Bets page
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after navigation to My Bets page
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure user has open (unsettled) bets
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def get_bet_by_name(self, bet_name):
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg=f'Bets are not found on "Open Bets" page')
        bet = bets.get(bet_name)
        self.assertTrue(bet, msg=f'Bet {bet_name} is not found in {bets.keys()}')
        return bet

    def test_001_navigate_to_my_bets_page(self, flg_login=True):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: - Open bets tab is opened
        EXPECTED: - Open bets are present
        """
        self.check_my_bets_counter_enabled_in_cms()

        event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.marketID = event.default_market_id
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids[event.team1]
        start_time = event.event_date_time
        start_time_local = self.convert_time_to_local(date_time_str=start_time,
                                                      future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.first_bet_name = f'SINGLE - [{event.team1} v {event.team2} {start_time_local}]'
        self.__class__.expected_betslip_counter_value = 0

        if flg_login:
            self.site.login(username=tests.settings.default_username)
        self.__class__.initial_counter = int(self.get_my_bets_counter_value_from_footer())

        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter + 1,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{self.initial_counter + 1}"')

    def test_002_verify_displaying_correct_my_bets_counter_when_number_of_my_bets_has_changed_after_cash_out(self):
        """
        DESCRIPTION: Verify displaying correct My Bets counter when number of My bets has changed after Cash Out
        EXPECTED: - My bets badge' icon is changed the number of unsettled bets in real time for Cash-out.
        EXPECTED: - Back-end request is send to BPP if 20+ bets is still present after cash-out (verify with *count?* search in devtools XHR tab)
        EXPECTED: - Back-end request is not send to BPP if less than 20 bets is still present after cash-out (verify with *count?* search in devtools XHR tab)
        """
        self.site.open_my_bets_cashout()
        bet = self.get_bet_by_name(self.first_bet_name)

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter,
                         msg=f'Actual value indicator "{counter_value}" != Expected "{self.initial_counter}"')

    def test_003_verify_displaying_correct_my_bets_counter_when_number_of_my_bets_has_changed_after_settling_of_the_users_bet(
            self):
        """
        DESCRIPTION: Verify displaying correct My Bets counter when number of My bets has changed after Settling of the user's bet
        EXPECTED: - My bets counter icon is changed the number of unsettled bets after navigation to other tab and back to Open bets for Settled Bets or New Bet added
        """
        self.test_001_navigate_to_my_bets_page(flg_login=False)
        self.result_event(event_id=self.eventID, market_id=self.marketID, selection_ids=self.selection_ids)
        expected_indicator = self.initial_counter + 1
        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, expected_indicator,
                         msg=f'My bets counter "{counter_value}" is not the same '
                             f'as expected "{expected_indicator}"')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage', timeout=15)
        wait_for_result(lambda: int(self.get_my_bets_counter_value_from_footer()) > 0, name='Wait for My Bets counter to load')

        counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, expected_indicator - 1, msg=f'My bets counter "{counter_value}" is not the same'
                                                                    f' as expected "{expected_indicator - 1}"')
