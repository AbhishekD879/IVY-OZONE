import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.login
@vtest
class Test_C489852_Full_Cash_Out_process_when_market_or_selection_becomes_undisplayed_for_Multiple_bet(BaseCashOutTest):
    """
    TR_ID: C489852
    NAME: Full Cash Out process when event/market/selection becomes undisplayed for Multiple bet
    DESCRIPTION: This test case verifies Cash Out process when event/market/selection becomes undisplayed
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of of pre-match events.
    PRECONDITIONS: (Currently works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker
    PRECONDITIONS: (other sports will be added in future).**
    """
    keep_browser_open = True
    events = None
    event1_name, event2_name, event3_name = None, None, None
    number_of_events = 3
    initial_cashout_value = None
    selections = {}
    bet_amount = 1
    match_result_id = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        self.__class__.events = self.create_several_autotest_premier_league_football_events(
            number_of_events=self.number_of_events)
        for event in self.events:
            self.__class__.selections.update({event.event_name: event.selection_ids[event.team1]})

        self.__class__.event1_name = f'{self.events[0].event_name} {self.events[0].local_start_time}'
        self.__class__.event2_name = f'{self.events[1].event_name} {self.events[1].local_start_time}'
        self.__class__.event3_name = f'{self.events[2].event_name} {self.events[2].local_start_time}'

        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=self.selections.values())
        self.place_multiple_bet(number_of_stakes=self.number_of_events)

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
        DESCRIPTION: Tap 'CASH OUT' button
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=[self.event1_name, self.event2_name], number_of_bets=self.number_of_events)
        self.__class__.initial_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        self.bet.buttons_panel.full_cashout_button.click()

    def test_003_trigger_undisplaying_in_openbet_ti_tool_for_current_event_market_selection(self):
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
        EXPECTED: *   Green box with "tick" in a circle and message of "CASH OUT SUCCESSFUL" are shown below bet line
        EXPECTED: details. The icon and text are centered within green box.
        EXPECTED: *   Underneath the green box, another message is displayed: "Your Cash Out attempt was successful
        EXPECTED: <currency symbol><value>." The text of message is centered.
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(outcome_name=self.bet_name)

    def test_005_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on cashed out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.initial_cashout_value))
        self.__class__.user_balance = self.site.header.user_balance

    def test_006_go_to_trixie_multiple_bet(self):
        """
        DESCRIPTION: Navigate to the **Multiple** bet and check cash out value on 'CASH OUT' button
        DESCRIPTION: Tap 'CASH OUT' button
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='TRIXIE', event_names=self.event2_name, number_of_bets=self.number_of_events)
        self.__class__.initial_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        self.bet.buttons_panel.full_cashout_button.click()

    def test_007_trigger_undisplaying_in_openbet_ti_tool_for_current_market(self):
        """
        DESCRIPTION: Trigger undisplaying in Openbet TI tool for current market
        EXPECTED: Market becomes undisplayed
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.match_result_id = self.ob_config.market_ids[self.events[1].event_id][market_short_name]
        self.ob_config.change_market_state(
            event_id=self.events[1].event_id, market_id=self.match_result_id, displayed=False, active=True)

    def test_008_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: *   Green box with "tick" in a circle and message of "CASH OUT SUCCESSFUL" are shown below bet line
        EXPECTED: details. The icon and text are centered within green box.
        EXPECTED: *   Underneath the green box, another message is displayed: "Your Cash Out attempt was successful
        EXPECTED: <currency symbol><value>." The text of message is centered.
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()
        self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(outcome_name=self.bet_name)

    def test_009_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on cashed out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.initial_cashout_value))
        self.__class__.user_balance = self.site.header.user_balance

    def test_010_go_to_patent_multiple_bet(self):
        """
        DESCRIPTION: Navigate to the **Multiple** bet and check cash out value on 'CASH OUT' button
        DESCRIPTION: Tap 'CASH OUT' button
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='TREBLE', event_names=self.event3_name, number_of_bets=self.number_of_events)
        self.__class__.initial_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        self.bet.buttons_panel.full_cashout_button.click()

    def test_011_trigger_undisplaying_in_openbet_ti_tool_for_current_event(self):
        """
        DESCRIPTION: Trigger undisplaying in Openbet TI tool for current event
        EXPECTED: Event becomes undisplayed
        """
        self.ob_config.change_event_state(event_id=self.events[2].event_id, displayed=False, active=True)

    def test_012_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: *   Green box with "tick" in a circle and message of "CASH OUT SUCCESSFUL" are shown below bet line
        EXPECTED: details. The icon and text are centered within green box.
        EXPECTED: *   Underneath the green box, another message is displayed: "Your Cash Out attempt was successful
        EXPECTED: <currency symbol><value>." The text of message is centered.
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        self.assertTrue(self.bet.wait_for_element_disappear(timeout=30),
                        msg=f'Bet is still present on Cashout page after cashout and refreshing the page')

    def test_013_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on cashed out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.initial_cashout_value))
