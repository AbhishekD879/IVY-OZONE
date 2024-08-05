import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C489944_Cash_Out_process_when_prices_change_cashoutValue_000_for_Multiple(BaseCashOutTest):
    """
    TR_ID: C489944
    NAME: Cash Out process when prices change (cashoutValue="0.00") for Multiple bet
    DESCRIPTION: This test case verifies Cash Out process when prices change
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has placed Multiple bets where Cash Out offer is available
    PRECONDITIONS: *   Open Dev tools -> Network tab -> XHR sorting type -> choose **getBetDetail?** / **getBetDetails?** request
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts, and Snooker (other sports will be added in future).**
    """
    keep_browser_open = True
    events = None
    event1_name, event2_name = None, None
    selections = {}
    bet_amount = 1
    correct_price = '4/1'
    incorrect_price = '400/1'
    expected_message = vec.bet_history.CASHOUT_BET.cashout_unavailable.bet_worth_nothing

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        self.__class__.events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.selections = {event.event_name: event.selection_ids[event.team1] for event in self.events}

        self.__class__.event1_name = f'{self.events[0].event_name} {self.events[0].local_start_time}'
        self.__class__.event2_name = f'{self.events[1].event_name} {self.events[1].local_start_time}'

        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=self.selections.values())
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_page_or_tab_on_betslip_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED:  'Cash Out' page / tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_multiple_bet_and_trigger_price_change_and_confirm_cash_out_buttons(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet line
        DESCRIPTION: Trigger price change in Openbet TI tool for current selection (e.g change price from 4/1 to 400/1)
        EXPECTED: Price is changed for selection
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=[self.event1_name, self.event2_name], number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')

        self.ob_config.change_price(self.selections[self.events[0].event_name], self.incorrect_price)

    def test_003_verify_error_message(self):
        """
        DESCRIPTION: Verify error messages
        EXPECTED: * The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: Message box with an "X" in a circle and message of 'CASH OUT NOT AVAILABLE' is shown below bet line details.
        EXPECTED: Underneath previous box second message is displayed with centered text 'Cash Out value of this bet is <currency symbol>0.00'
        """
        result = wait_for_result(lambda: self.bet.cash_out_error_message == self.expected_message,
                                 name=f'Wait for error message "{self.expected_message}" appear', timeout=15)
        self.assertTrue(result, msg=f'Actual message: "{self.bet.cash_out_error_message}" '
                                    f'is not as expected: "{self.expected_message}"')

    def test_004_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Multiple bet is shown with the same error message as in step #3
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()

        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=[self.event1_name, self.event2_name], number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.test_003_verify_error_message()

    def test_005_in_ob_backoffice_return_price_for_events_selection_to_the_previous_value(self):
        """
        DESCRIPTION: In OB Backoffice return price for event's selection to the previous value
        EXPECTED: * 'CASH OUT' button and slider are shown under bet details instead of error message
        """
        self.ob_config.change_price(self.selections[self.events[0].event_name], self.correct_price)

        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=[self.event1_name, self.event2_name], number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.assertFalse(self.bet.has_cash_out_error_message(expected_result=False),
                         msg='Cash Out error message is still displayed')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='Full Cash Out button is not shown')
