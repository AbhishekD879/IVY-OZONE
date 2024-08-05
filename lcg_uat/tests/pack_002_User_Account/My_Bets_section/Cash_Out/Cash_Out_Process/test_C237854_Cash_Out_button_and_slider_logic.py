from random import choice

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2  # disabled Partial Cashout tests on TST2/STG2 endpoints
# @pytest.mark.stg2  # due to offers constantly granted to user that prevents partial cashout appearance
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.cash_out
@pytest.mark.timeout(900)
@pytest.mark.slow
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C237854_Cash_Out_button_and_slider_logic(BaseCashOutTest):
    """
    TR_ID: C237854
    NAME: Cash Out button and slider logic for Single bets
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles bets where Cash Out offer is available
    PRECONDITIONS: * In order to trigger unavailable Partial Cash Out place a bet with small amount
    """
    keep_browser_open = True
    events = None
    event1_name, event2_name = None, None
    start_stake_amount = None
    start_est_returns = None
    bet = None
    stake_bet_amounts = 1
    bet_name = None
    number_of_events = 3
    selection_ids_all_events, selection_ids_no_partial_cashout = None, None
    event_ids = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            for event_id in cls.event_ids:
                ob_config.change_event_cashout_status(event_id=event_id, cashout_available=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        if tests.settings.backend_env == 'prod':
            user = tests.settings.betplacement_user
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter)
            if len(events) < 3:
                raise SiteServeException(
                    f'No enough active events for category id "{self.ob_config.football_config.category_id}"')

            # Event 1
            event = choice(events)
            events.remove(event)
            self.__class__.eventID = event['event']['id']
            self.__class__.event1_name = normalize_name(event['event']['name'])
            self.__class__.event_start_time = self.convert_time_to_local(
                date_time_str=event['event']['startTime'],
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True)
            outcomes = next((market['market']['children'] for market in event['event']['children']
                             if market['market']['templateMarketName'] == 'Match Betting' and
                             market['market'].get('children')), [])
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException(f'No home team for event "{self.event1_name}" with id "{self.eventID}"')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            if not selection_ids:
                raise SiteServeException(f'Outcomes list is empty for event "{self.event1_name}"')

            # Event 2
            event = choice(events)
            events.remove(event)
            self.__class__.eventID_2 = event['event']['id']
            self.__class__.event2_name = normalize_name(event['event']['name'])
            self.__class__.event_2_start_time = self.convert_time_to_local(
                date_time_str=event['event']['startTime'],
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True)
            outcomes_2 = next((market['market']['children'] for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Match Betting' and
                               market['market'].get('children')), [])
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes_2 if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team2:
                raise SiteServeException(f'No home team for event "{self.event2_name}" with id "{self.eventID_2}"')

            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}
            if not selection_ids2:
                raise SiteServeException(f'Outcomes list is empty for event "{self.event2_name}""')

            self.__class__.selection_ids_all_events = [selection_ids[self.team1], selection_ids2[self.team2]]

            # Event 3
            event = choice(events)
            events.remove(event)
            self.__class__.eventID_3 = event['event']['id']
            self.__class__.event3_name = normalize_name(event['event']['name'])
            self.__class__.event_3_start_time = self.convert_time_to_local(
                date_time_str=event['event']['startTime'],
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True)
            outcomes_3 = next((market['market']['children'] for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Match Betting' and
                               market['market'].get('children')), [])
            self.__class__.team3 = next((outcome['outcome']['name'] for outcome in outcomes_3 if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team3:
                raise SiteServeException(f'No home team for event "{self.event3_name}" with id "{self.eventID_3}"')

            selection_ids3 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_3}
            if not selection_ids3:
                raise SiteServeException(f'Outcomes list is empty for event "{self.event3_name}""')

            self.__class__.selection_ids_all_events = [selection_ids[self.team1], selection_ids2[self.team2],
                                                       selection_ids3[self.team3]]
        else:
            self.__class__.events = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            self.__class__.event1_name = f'{self.events[0].event_name} {self.events[0].local_start_time}'
            self.__class__.event2_name = f'{self.events[1].event_name} {self.events[1].local_start_time}'
            self.__class__.event3_name = f'{self.events[2].event_name} {self.events[2].local_start_time}'
            self.__class__.selection_ids_all_events = [event.selection_ids[event.team1] for event in self.events]
            self.__class__.event_ids = [event.event_id for event in self.events]
            user = tests.settings.betplacement_user

        self.site.login(username=user, async_close_dialogs=False)

        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events[:2])
        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events)
        self.place_multiple_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

        # To remove selection id's from URL (betslip/add/...) due to which test fails on step 10
        if self.device_type == 'desktop':
            self.site.go_to_home_page()

    def test_001_navigate_to_cash_out_tab_on_my_bets(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Cash Out' tab is opened
        EXPECTED: * 'PARTIAL CASHOUT' slider is not shown
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=bet_type, event_names=self.event1_name, number_of_bets=5)
        self.assertFalse(self.bet.buttons_panel.has_partial_cashout_slider, msg=f'PARTIAL CASHOUT slider is present for '
                                                                                f'"{bet_type} - {self.event1_name}"')

    def test_002_navigate_to_single_bet_line_click_on_the_cash_out_currency_symbol(self):
        """
        DESCRIPTION: * Navigate to **Single** bet line
        DESCRIPTION: * Click on the 'CASH OUT <currency symbol><value>' button and wait
        EXPECTED: * Button updates with the following centered text 'CONFIRM CASH OUT: <currency symbol><value>'
        EXPECTED: * 'PARTIAL CASHOUT' is disappeared from CASHOUT bar
        EXPECTED: * 'Confirm Cash Out' button has expired, becomes orange 'Cash Out <currency symbol><value>'
        EXPECTED: button until user clicks on Cash Out button again
        EXPECTED: Cash Out and Partial CashOut buttons revert to normal and are updated to the correct value/status
        """
        cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + ' £{0:.2f}'.format(cashout_amount)
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Actual text: "{confirmation_text}" is not as expected: "{expected_confirmation}"')

        self.bet.buttons_panel.full_cashout_button.wait_for_element_disappear()

        cash_out_text = self.bet.buttons_panel.full_cashout_button.name
        expected_cash_out_text = vec.bet_history.CASHOUT_BET.cash_out + ' £{0:.2f}'.format(cashout_amount)
        self.assertEqual(expected_cash_out_text, cash_out_text,
                         msg=f'Actual text: "{cash_out_text}" is not as expected: "{expected_cash_out_text}"')

        self.__class__.user_balance = self.site.header.user_balance

    def test_003_click_on_the_cash_out_button_and_click_on_confirm_cash_out(self):
        """
        DESCRIPTION: Click on the 'CASH OUT' button and click on 'CONFIRM CASH OUT'
        EXPECTED: Cashout success message is displayed, bet is not displayed on page
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(timeout=20),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(outcome_name=self.bet_name)

    def test_004_navigate_to_another_single_bet_and_click_on_partial_cashout_button(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to another Single bet and click on 'PARTIAL CASHOUT' button
        EXPECTED: 'PARTIAL CASHOUT' slider is shown
        """
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=bet_type, event_names=self.event2_name, number_of_bets=5)
        self.bet.scroll_to()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg=f'PARTIAL CASHOUT button is not present for "{bet_type} - {self.event2_name}". Check "bet-details" response "cashoutValue" parameter value')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg=f'PARTIAL CASHOUT slider has not appeared for '
                                                                              f'"{bet_type} - {self.event2_name}"')

    def test_005_click_on_x_button_on_cashout_bar(self):
        """
        DESCRIPTION: Click on 'X' button on CASHOUT bar
        EXPECTED: * 'PARTIAL CASHOUT' slider is hidden
        EXPECTED: * 'CASH OUT <currency symbol><value>' button is shown instead
        EXPECTED: * 'PARTIAL CASHOUT' is shown on CASHOUT bar
        """
        self.bet.buttons_panel.partial_cashout_close_button.click()
        self.assertFalse(self.bet.buttons_panel.wait_for_cashout_slider(expected_result=False),
                         msg='PARTIAL CASHOUT slider is present')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='FULL CASHOUT button is not present')
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg='PARTIAL CASHOUT button is not present or '
                            'check "bet-details" response "cashoutValue" parameter value')

    def test_006_click_on_partial_cashout_button_again(self):
        """
        DESCRIPTION: Click on 'PARTIAL CASHOUT' button again
        EXPECTED: 'PARTIAL CASHOUT' slider has appeared
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()

    def test_007_move_slider(self):
        """
        DESCRIPTION: Move slider
        EXPECTED: * The 'Pointer'moves on the Bar
        EXPECTED: * The Cash Out value is automatically updated in the Cash Out button
        EXPECTED: * Partial Cash Out value is rounded to the nearest 2 decimal places
        """
        # TODO: VOL-3738 to cover it

    def test_008_set_pointer_on_the_bar_to_any_value_and_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Partial CashOut slider is hidden
        """
        # TODO: VOL-3738 to cover it

    def test_009_set_pointer_on_the_bar_to_any_percentage_value_not_to_100_and_navigate_to_other_page(self):
        """
        DESCRIPTION: Navigate to other page/tab.
        DESCRIPTION: Navigate back to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget.
        EXPECTED: Partial CashOut slider is hidden for all bets on page
        """
        # TODO: VOL-3738 to cover it

    def test_010_navigate_to_bet_line_with_unavailable_partial_cash_out(self):
        """
        DESCRIPTION: Navigate to bet line with unavailable Partial Cash Out
        EXPECTED: 'PARTIAL CASHOUT' button is not shown on CASHOUT bar
        """
        self.__class__.bet_amount = 0.05
        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events[0])

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()
        bet_name, bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event1_name, number_of_bets=1)
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False, timeout=5),
                         msg=f'PARTIAL CASHOUT button is present for "{bet_name}". It should not.')

    def test_011_repeat_steps_1_10_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #1-10 for **Multiple** bet
        """
        self.__class__.bet_amount = 2.5
        self.test_001_navigate_to_cash_out_tab_on_my_bets(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.test_002_navigate_to_single_bet_line_click_on_the_cash_out_currency_symbol()
        self.test_003_click_on_the_cash_out_button_and_click_on_confirm_cash_out()
        self.test_004_navigate_to_another_single_bet_and_click_on_partial_cashout_button(bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE)
        self.test_005_click_on_x_button_on_cashout_bar()
        self.test_006_click_on_partial_cashout_button_again()
        self.test_007_move_slider()
        self.test_008_set_pointer_on_the_bar_to_any_value_and_refresh_page()
        self.test_009_set_pointer_on_the_bar_to_any_percentage_value_not_to_100_and_navigate_to_other_page()

        self.__class__.bet_amount = 0.10
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events[:2])
        self.place_multiple_bet(number_of_stakes=1)

        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()

        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                                                                              event_names=self.event1_name,
                                                                              number_of_bets=5)
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg=f'PARTIAL CASHOUT button is present for "{bet_name}". It should not.')
