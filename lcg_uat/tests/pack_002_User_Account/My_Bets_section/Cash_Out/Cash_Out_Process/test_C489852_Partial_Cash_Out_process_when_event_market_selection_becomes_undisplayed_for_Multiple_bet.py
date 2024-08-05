import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-47840')  # Ladbrokes dev0 BPP
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1708')
@pytest.mark.login
@vtest
class Test_C489852_Partial_Cash_Out_process_when_market_or_selection_becomes_undisplayed_for_Multiple_bet(BaseCashOutTest):
    """
    TR_ID: C489852
    NAME: Partial Cash Out process when event/market/selection becomes undisplayed for Multiple bet
    DESCRIPTION: This test case verifies Cash Out process when event/market/selection becomes undisplayed
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    """
    keep_browser_open = True
    selections = {}
    bet_amount = 1
    number_of_events = 2
    event1_name, event2_name = None, None
    initial_cashout_value, match_result_id, events = None, None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        self.__class__.events = self.create_several_autotest_premier_league_football_events(
            number_of_events=self.number_of_events)
        self.__class__.selections = {event.event_name: event.selection_ids[event.team1] for event in self.events}
        self.__class__.event1_name = f'{self.events[0].event_name} {self.events[0].local_start_time}'
        self.__class__.event2_name = f'{self.events[1].event_name} {self.events[1].local_start_time}'

        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=self.selections.values())
        self.place_multiple_bet()

        self.site.bet_receipt.footer.click_done()
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_navigate_to_cash_out_page_or_tab_on_betslip_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_double_multiple_bet(self):
        """
        DESCRIPTION: Navigate to the **Multiple** bet and check cash out value on 'CASH OUT' button
        DESCRIPTION: Tap 'PARTIAL CASHOUT' button
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=[self.event1_name, self.event2_name], number_of_bets=4)
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg='PARTIAL CASHOUT button is not present or '
                            'check "bet-details" response "cashoutValue" parameter value')

        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()

        self.__class__.initial_cashout_value = self.bet.buttons_panel.partial_cashout_button.amount.value

    def test_003_trigger_undisplaying_in_openbet_ti_tool_for_current_selection(self):
        """
        DESCRIPTION: Trigger undisplaying in Openbet TI tool for current selection
        EXPECTED: Selection becomes undisplayed
        """
        self.ob_config.change_selection_state(
            selection_id=self.selections[self.events[0].event_name], displayed=False, active=True)

    def test_004_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: *   Green box with "tick" in a circle and message of "CASH OUT SUCCESSFUL" are shown below bet line details. The icon and text are centered within green box.
        EXPECTED: *   Underneath the green box, another message is displayed: "Your Cash Out attempt was successful <currency symbol><value>." The text of message is centered.
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        success_message = self.bet.cash_out_successful_message
        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertEqual(success_message, expected_message,
                         msg=f'Success message "{success_message}" is not the same as expected: "{expected_message}"')

    def test_005_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on cashed out value
        """
        self.device.refresh_page()
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.initial_cashout_value))
