from math import ceil
from random import choice

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2  # disabled Partial Cashout tests on TST2/STG2 endpoints
# @pytest.mark.stg2  # due to offers constantly granted to user that prevents partial cashout appearance
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C237690_Successful_Partial_Cash_Out_Process(BaseCashOutTest):
    """
    TR_ID: C237690
    NAME: Successful Partial Cash Out process
    DESCRIPTION: This test case verifies successful Partial Cash Out process on 'Cash Out' tab
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Multiple bets where Cash Out offer is available
    PRECONDITIONS: * CORAL:
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: * Ladbrokes:
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of of pre-match events. (Currently works as for in-play events)
    """
    keep_browser_open = True
    start_stake_amount = None
    start_est_returns = None
    bet = None
    bet_name = None
    bet_amount = 0.5
    events = None
    number_of_events = 2
    selection_ids_all_events = None
    event_ids = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            for event_id in cls.event_ids:
                ob_config.change_event_cashout_status(event_id=event_id, cashout_available=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test football event, PROD: Find active Football events
        DESCRIPTION: Login as user that has funds to place a bet
        DESCRIPTION: Place bets
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            # event 1
            event1 = choice(events)
            events.remove(event1)
            self.__class__.eventID = event1['event']['id']
            self.__class__.created_event_name = normalize_name(event1['event']['name'])
            self.__class__.event_start_time = self.convert_time_to_local(date_time_str=event1['event']['startTime'],
                                                                         ob_format_pattern=self.ob_format_pattern,
                                                                         future_datetime_format=self.event_card_future_time_format_pattern)
            match_result_market = next((market['market'] for market in event1['event']['children']
                                        if market.get('market').get('templateMarketName') == 'Match Betting'), None)
            if not match_result_market:
                raise SiteServeException(f'Event {self.eventID} does not have Match Result Market')
            outcomes = match_result_market['children']
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException(f'There is no "Home" team available for event with id "{self.eventID}"')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.info(f'Event name: "{self.created_event_name}" id: "{self.eventID}" '
                              f'team name: "{self.team1}" start time: "{self.event_start_time}" '
                              f'selection ids: "{selection_ids}"')

            # event 2
            event2 = choice(events)
            events.remove(event2)
            self.__class__.eventID_2 = event2['event']['id']
            self.__class__.created_event_2_name = normalize_name(event2['event']['name'])
            self.__class__.event_2_start_time = self.convert_time_to_local(date_time_str=event2['event']['startTime'],
                                                                           ob_format_pattern=self.ob_format_pattern,
                                                                           future_datetime_format=self.event_card_future_time_format_pattern)
            match_result_market2 = next((market['market'] for market in event2['event']['children']
                                         if market.get('market').get('templateMarketName') == 'Match Betting'), None)
            if not match_result_market2:
                raise SiteServeException(f'Event {self.eventID_2} does not have Match Result Market')
            outcomes_2 = match_result_market2['children']
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes_2 if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team2:
                raise SiteServeException(f'There is no "Away" team available for event with id "{self.eventID_2}')
            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}
            self._logger.info(f'Event name: "{self.created_event_2_name}" id: "{self.eventID_2}" '
                              f'team name: "{self.team2}" start time: "{self.event_2_start_time}" '
                              f'selection ids: "{selection_ids2}"')

            self.__class__.selection_ids_all_events = [selection_ids[self.team1], selection_ids2[self.team2]]
        else:
            self.__class__.events = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events, bir_delay=10, is_live=True)
            self.__class__.selection_ids_all_events = [event.selection_ids[event.team1] for event in self.events]
            self.__class__.event_ids = [event.event_id for event in self.events]

        self.site.login(async_close_dialogs=False)

        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_cash_out_tab_on_my_bets(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Cash Out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_single_cashout_bet_line(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to **Single** bet line
        EXPECTED: 'Partial CashOut' slider is shown
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=bet_type, number_of_bets=2)

    def test_003_click_on_partial_cashout_button_on_cashout_bar(self):
        """
        DESCRIPTION: Click on 'Partial CashOut' button on CashOut bar
        EXPECTED: 'Partial CashOut' slider is shown
        """
        self.__class__.start_stake = float(self.bet.stake.stake_value)
        self.__class__.start_est_returns_amount = float(self.bet.est_returns.stake_value)
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')

    def test_004_set_pointer_on_the_bar_to_any_value_not_to_maximum(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum)
        EXPECTED: Value on CashOut button is changed
        """
        # TODO: VOL-3738 to cover it

    def test_005_tap_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button and verify that 'CONFIRM CASH OUT' button is shown
        EXPECTED: 'CONFIRM CASH OUT' button is shown
        """
        self.__class__.cashout_amount = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.bet.buttons_panel.partial_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + ' £{0:.2f}'.format(self.cashout_amount)
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')

    def test_006_trigger_happy_cash_out_page_and_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Trigger happy cash out path (e.g. cash out value remains unchanged)
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner icon with countdown timer (Timer is available from OX 99) in format XX:XX (countdown timer is
        EXPECTED:  taken from 'cashoutBet' response: 'cashoutDelay attribute value) appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        self.bet.buttons_panel.cashout_button.click()

        """ imho we cannot automate wait for timer and spinner - sometimes cashoutDelay is too low"""
        # TODO VOL-5375
        # result = self.bet.buttons_panel._spinner_wait(expected_result=True, timeout=1)
        # self.assertTrue(result, msg='Spinner not found')
        #
        # timer = self.bet.buttons_panel.timer.text
        # self.assertRegex(timer, r'\d{2}:\d{2}', msg=f'Countdown timer "{timer}" has incorrect format. '
        #                                             f'Expected format: "XX:XX"')

    def test_007_wait_until_button_with_spinner_and_countdown_timer_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner and countdown timer (Timer is available from OX 99) disappears
        EXPECTED: The success message is displayed below 'CASH OUT' button "Partial Cashout Successful"
        EXPECTED: Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        """
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message, timeout=20),
                        msg=f'Message "{expected_message}" is not shown')

        expected_stake = str(ceil(self.start_stake * 0.5 * 100) / 100)

        result = wait_for_result(lambda: str(self.bet.stake.stake_value) == expected_stake,
                                 name='Stake value to change',
                                 timeout=1)

        self.assertTrue(result, msg=f'Bet: "{self.bet_name}" Cash Out value after partial cash out is: '
                        f'"{str(self.bet.stake.stake_value)}", expected: "{expected_stake}"')

        actual_est_returns = float(self.bet.est_returns.stake_value)
        expected_est_returns = float(str(ceil(self.start_est_returns_amount * 0.5 * 100) / 100))
        delta = 0.03
        self.assertAlmostEqual(actual_est_returns, expected_est_returns, delta=delta,
                               msg=f'Actual Estimated returns: "{actual_est_returns}" '
                                   f'does not match with excepted: "{expected_est_returns}" with delta "{delta}"')

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on previously cashed out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount),
                                 timeout=10)

    def test_009_navigate_to_multiple_cash_out_bet_line(self):
        """
        DESCRIPTION: Navigate to **Multiple** Cash Out bet line
        """
        self.test_002_go_to_single_cashout_bet_line(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)

    def test_010_repeat_steps_3_8_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps #3-8 for Multiple Cash Out bet lines
        """
        self.test_003_click_on_partial_cashout_button_on_cashout_bar()
        self.test_004_set_pointer_on_the_bar_to_any_value_not_to_maximum()
        self.test_005_tap_cash_out_button()
        self.test_006_trigger_happy_cash_out_page_and_tap_confirm_cash_out_button()
        self.test_007_wait_until_button_with_spinner_and_countdown_timer_disappears()
        self.test_008_verify_user_balance()
