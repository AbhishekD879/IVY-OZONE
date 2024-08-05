import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.build_your_bet
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C2507465_full_cash_out_of_banach_bet(BaseBanachTest):
    """
    TR_ID: C2507465
    NAME: Full cash out of Banach bet
    DESCRIPTION: Test case verifies full Cash out of Banach bet
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab
    PRECONDITIONS: in Dev tools > Network find getBetDetails request > identify bet by betID
    PRECONDITIONS: User has placed Banach bet(s)
    PRECONDITIONS: Banach bet is displayed on Cash out tab
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 0.1
    blocked_hosts = ['*spark-br.*']
    event_start_time_local = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Place Banach bet
        """
        self.site.login()
        self.site.wait_content_state('homepage')
        self.__class__.eventID = self.get_ob_event_with_byb_market()

        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                  query_builder=self.ss_query_builder)
        event_start_time = event_details[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.event_card_future_time_format_pattern,
            ss_data=True)

        self.__class__.event_name = normalize_name(event_details[0]['event']['name'])

        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'"{self.expected_market_sections.match_betting}" market does not exist')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market, msg=f'"{self.expected_market_sections.both_teams_to_score}" market does not exist')
        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip has not appeared')
        byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(byb_betslip_panel, msg='BYB BetSlip is not shown')
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)
        try:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')
        except VoltronException:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='Build Your Bet Bet Receipt NOT displayed')

        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_byb_bet_receipt_panel(expected_result=False),
                         msg='Build Your Bet Bet Receipt still displayed')

        self.__class__.user_balance = self.site.header.user_balance

    def test_001_navigate_to_my_bets_cashout_and_verify_cash_out_button_value(self):
        """
        DESCRIPTION: Navigate to My Bets > Cash-out and verify Cash out button value
        EXPECTED: The amount eligible for cash out displayed on the button is taken from cashoutValue parameter of getBetDetails request
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Event: "{self.event_name}" Single bet not found')
        self.__class__.expected_cashout_value = self.bet_amount - (self.bet_amount * 0.1)
        actual_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        self.softAssert(self.assertEqual, float(actual_cashout_value), self.expected_cashout_value,
                        msg=f'Actual cash out value: "{actual_cashout_value}", '
                        f'expected: "{self.expected_cashout_value}"')

    def test_002_tap_on_cash_out_button(self):
        """
        DESCRIPTION: Tap on CASH OUT button
        EXPECTED: Confirm cash out % button is shown, where % is cashoutValue parameter of getBetDetails request
        """
        self.__class__.buttons_panel = self.bet.buttons_panel
        self.buttons_panel.full_cashout_button.click()
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + \
            ' £{0:.2f}'.format(self.expected_cashout_value)
        result = wait_for_result(lambda: self.buttons_panel.cashout_button.name == expected_confirmation,
                                 expected_result=True,
                                 name='Expiry date to change',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'Expected confirmation text: "{expected_confirmation}" '
                        f'is not equal to actual: "{self.buttons_panel.cashout_button.name}"')

    def test_003_confirm_cash_out(self):
        """
        DESCRIPTION: Confirm cash out
        EXPECTED: Successful cash out notification is displayed
        EXPECTED: User balance is updated
        EXPECTED: Bet disappears from Cash Out page after page reload
        """
        wait_for_result(lambda: self.bet.buttons_panel.full_cashout_button.is_displayed(),
                        timeout=5,
                        name='Confirmation text to disappear')
        self.buttons_panel.full_cashout_button.click()
        self.buttons_panel.cashout_button.click()

        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

        self.verify_user_balance(expected_user_balance=self.user_balance + self.expected_cashout_value)

        self.device.refresh_page()
        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()

        result = self.site.cashout.tab_content.accordions_list.wait_till_bet_disappear(self.bet_name, timeout=7)
        self.assertTrue(result, msg=f'Bet: "{self.bet_name}" is still displayed after reloading the page')