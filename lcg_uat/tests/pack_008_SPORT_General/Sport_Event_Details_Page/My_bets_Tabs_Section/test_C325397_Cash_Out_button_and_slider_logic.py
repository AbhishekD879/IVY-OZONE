import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from random import choice
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2 # Applicable only for Prod
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.cash_out
@vtest
class Test_C325397_Cash_Out_button_and_slider_logic(BaseCashOutTest):
    """
    TR_ID: C325397
    NAME: Cash Out button and slider logic.
    DESCRIPTION: The test case needs to be edited according to the latest changes+Vanilla changes.
    DESCRIPTION: This test case verifies Cash Out button and slider logic on 'My Bets' tab on Event Details page
    DESCRIPTION: *Jira Tickets:*
    DESCRIPTION: [BMA-24365 My Bets Improvement : CashOut: Redesign of main cashout CTA Partial Cashout] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24365
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
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
        user = tests.settings.betplacement_user
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id, all_available_events=True, additional_filters=cashout_filter)
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
        if self.device_type == 'desktop':
            self.site.go_to_home_page()

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * 'PARTIAL CASHOUT' slider is not shown
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=bet_type, event_names=self.event1_name, number_of_bets=5)
        self.assertFalse(self.bet.buttons_panel.has_partial_cashout_slider,
                         msg=f'PARTIAL CASHOUT slider is present for '
                             f'"{bet_type} - {self.event1_name}"')

    def test_002__navigate_to_single_bet_line_click_on_the_cash_out_currency_symbolvalue_button_and_wait(self):
        """
        DESCRIPTION: * Navigate to **Single** bet line
        DESCRIPTION: * Click on the 'CASH OUT <currency symbol><value>' button and wait
        EXPECTED: * Button updates with the following centered text 'CONFIRM CASH OUT: <currency symbol><value>' and becomes green
        EXPECTED: * 'PARTIAL CASHOUT' is disappeared from CASHOUT bar
        EXPECTED: * The Cash Out button displays with 'CONFIRM CASH OUT' for a maximum of 6200ms
        EXPECTED: * 'Confirm Cash Out' button flashes three times when time is running out
        EXPECTED: * 'Confirm Cash Out' button has expired, becomes 'Cash Out <currency symbol><value>' button until user clicks on Cash Out button again
        EXPECTED: * Cash Out and Partial CashOut buttons revert to normal and are updated to the correct value/status
        EXPECTED: **Note:** Old pop-up with confirmation message doesn't appear
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

    def test_003_1_click_on_the_cash_out_currency_symbolvalue_button_and_trigger_error_cashout_seln_suspended_for_bet_via_liveserve_update_suspend_event_or_market_or_selection_for_event_with_placed_bet2_click_cashout_button_confirm_cashout_and_simultaneously_trigger_cashoutvalue_cashout_seln_no_cashout_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_tool(self):
        """
        DESCRIPTION: 1) Click on the 'CASH OUT <currency symbol><value>' button and trigger error "CASHOUT_SELN_SUSPENDED" for bet via LiveServe update (Suspend event or market or selection for event with placed bet)
        DESCRIPTION: 2) Click 'Cashout' button, confirm cashout and simultaneously trigger cashoutValue: "CASHOUT_SELN_NO_CASHOUT" in getbetDetail response for Single Cash Out bet (e.g. mock response with Fiddler tool)
        EXPECTED: Flashing stops and error is shown immediately as described in TC 238033 or TC 237389
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

    def test_004_click_on_the_cash_out_button_and_click_on_confirm_cash_out(self):
        """
        DESCRIPTION: Click on the 'CASH OUT' button and click on 'CONFIRM CASH OUT'
        EXPECTED: * The Cash Out attempt is sent to OpenBet (cashoutBet request is sent, can be checked in Network tab)
        EXPECTED: * Spinner is displayed centered
        """
        # Covered in step 3

    def test_005__navigate_to_another_single_bet_click_on_partial_cashout_button_and_move_slider_on_the_bar(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: * Navigate to another Single bet
        DESCRIPTION: * Click on 'PARTIAL CASHOUT' button and move slider on the bar
        EXPECTED: * Pointer on the Bar moves left or right
        EXPECTED: * Value on CashOut button is changed
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=bet_type, event_names=self.event2_name, number_of_bets=5)
        bet.scroll_to()
        self.assertTrue(bet.buttons_panel.has_partial_cashout_button(),
                        msg=f'PARTIAL CASHOUT button is not present for "{bet_type} - {self.event2_name}". Check "bet-details" response "cashoutValue" parameter value')
        bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(bet.buttons_panel.wait_for_cashout_slider(),
                        msg=f'PARTIAL CASHOUT slider has not appeared for '
                            f'"{bet_type} - {self.event2_name}"')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(outcome_name=self.bet_name)
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=bet_type, event_names=self.event2_name, number_of_bets=5)
        bet.scroll_to()
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg='FULL CASHOUT button is not present')
        self.assertTrue(bet.buttons_panel.has_partial_cashout_button(),
                        msg=f'PARTIAL CASHOUT button is not present for "{bet_type} - {self.event2_name}". Check "bet-details" response "cashoutValue" parameter value')

    def test_006_set_pointer_on_the_slider_to_any_percentage_value_and_refresh_page(self):
        """
        DESCRIPTION: Set pointer on the slider to any percentage value and refresh page
        EXPECTED: 'CASH OUT <currency symbol><value>' and 'PARTIAL CASHOUT' are seen on CASHOUT bar
        """
        # Covered in step 5

    def test_007_set_pointer_on_the_slider_to_any_percentage_value_and_navigate_to_other_pagetabnavigate_back_to_my_bets_tab_on_event_details_page(self):
        """
        DESCRIPTION: Set pointer on the slider to any percentage value and navigate to other page/tab
        DESCRIPTION: Navigate back to 'My Bets' tab on Event Details page
        EXPECTED: 'CASH OUT <currency symbol><value>' and 'PARTIAL CASHOUT' are seen on CASHOUT bar
        """
        # Covered in step 6

    def test_008_navigate_to_bet_line_with_unavailable_partial_cash_out(self):
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

    def test_009_repeat_steps_2_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-8 for **Multiple** bet
        EXPECTED:
        """
        self.__class__.bet_amount = 2.5
        self.test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.test_002__navigate_to_single_bet_line_click_on_the_cash_out_currency_symbolvalue_button_and_wait()
        self.test_003_1_click_on_the_cash_out_currency_symbolvalue_button_and_trigger_error_cashout_seln_suspended_for_bet_via_liveserve_update_suspend_event_or_market_or_selection_for_event_with_placed_bet2_click_cashout_button_confirm_cashout_and_simultaneously_trigger_cashoutvalue_cashout_seln_no_cashout_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_tool()
        self.test_004_click_on_the_cash_out_button_and_click_on_confirm_cash_out()
        self.test_005__navigate_to_another_single_bet_click_on_partial_cashout_button_and_move_slider_on_the_bar(bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE)
        self.test_006_set_pointer_on_the_slider_to_any_percentage_value_and_refresh_page()
        self.test_007_set_pointer_on_the_slider_to_any_percentage_value_and_navigate_to_other_pagetabnavigate_back_to_my_bets_tab_on_event_details_page()
        self.__class__.bet_amount = 0.05
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events[:2])
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_names=self.event1_name,
            number_of_bets=5)
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg=f'PARTIAL CASHOUT button is present for "{bet_name}". It should not.')
