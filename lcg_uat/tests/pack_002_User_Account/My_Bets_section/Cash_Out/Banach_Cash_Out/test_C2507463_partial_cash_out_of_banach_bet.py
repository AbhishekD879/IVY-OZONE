import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import get_cashout_value


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
@pytest.mark.reg167_fix
@vtest
@pytest.mark.issue("https://jira.egalacoral.com/browse/BMA-55778")
class Test_C2507463_Partial_cash_out_of_Banach_bet(BaseBanachTest):
    """
    TR_ID: C2507463
    NAME: Partial cash out of Banach bet
    DESCRIPTION: Test case verifies Partial cash out of Banach bet
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab
    PRECONDITIONS: in Dev tools > Network find getBetDetails request > identify bet by betID
    PRECONDITIONS: User has placed Banach bet(s)
    PRECONDITIONS: Banach bet is displayed on Cash out tab
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 0.4
    event_start_time_local = None
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Place Banach bet
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        byb_markets = self.cms_config.get_build_your_bet_markets()
        markets_list = [market['bybMarket'] for market in byb_markets]
        if self.expected_market_sections.match_betting.title() and self.expected_market_sections.both_teams_to_score.title() \
                not in markets_list:
            raise CmsClientException(f'BYB Markets "{self.expected_market_sections.match_betting.title()}" or '
                                     f'"{self.expected_market_sections.both_teams_to_score.title()}" was not found')
        username = tests.settings.betplacement_user
        self.site.login(username=username)

        self.navigate_to_edp(event_id=self.eventID)

        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
                        msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_time_resp = event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               future_datetime_format=self.event_card_future_time_format_pattern,
                                                               ss_data=True)
        self.__class__.event_name = f'{event_resp[0]["event"]["name"]} {event_time_resp_converted}' if self.brand == 'ladbrokes' else event_resp[0]['event']['name']

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
        self.assertTrue(both_teams_to_score_market,
                        msg=f'"{self.expected_market_sections.both_teams_to_score}" market does not exist')
        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='Build Your Bet Betslip not appears')
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)

        self.site.byb_betslip_panel.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                        msg='Build Your Bet Bet Receipt NOT displayed')

        self.site.byb_bet_receipt_panel.header.close_button.click()

    def test_001_navigate_to_my_bets_cashout_and_verify_cash_out_button_value(self):
        """
        DESCRIPTION: Navigate to My Bets > Cash-out and verify Cash out button value
        EXPECTED: Cash Out Button contains Partial cash-out option if getBetDetails has parameter partialCashoutAvailable: "Y"
        EXPECTED: The amount eligible for cash out displayed on the button is taken from cashoutValue parameter of getBetDetails request
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Event: "{self.event_name}" Single bet not found')
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg='PARTIAL CASHOUT button is not present or '
                            'check "bet-details" response "cashoutValue" parameter value')
        self.__class__.expected_cashout_value = get_cashout_value()
        self.__class__.user_balance = self.site.header.user_balance
        actual_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        self.assertEqual(float(actual_cashout_value), float(self.expected_cashout_value),
                         msg=f'Actual cash out value: "{actual_cashout_value}", '
                             f'expected: "{self.expected_cashout_value}"')

    def test_002_tap_partial_cash_out(self):
        """
        DESCRIPTION: Tap partial cash out
        EXPECTED: The slider is opened with default value in the middle
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')

    def test_003_tap_on_cash_out(self):
        """
        DESCRIPTION: Tap on Cash out
        EXPECTED: Confirm Cash out button is shown with correct value cashoutValue parameter of getBetDetails request divided by 2)
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        self.__class__.partial_cashout_value = float(self.expected_cashout_value) / 2
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + ' £{0:.2f}'.format(self.partial_cashout_value)
        self.assertEqual(expected_confirmation, confirmation_text, msg=f'Confirmation text: "{expected_confirmation}" '
                                                                       f'is not equal to actual: "{confirmation_text}"')

    def test_004_approve_cashout(self):
        """
        DESCRIPTION: Approve cashout
        EXPECTED: Successful cash out notification is displayed
        EXPECTED: User balance is increased accordingly by cashed out amount
        EXPECTED: Bet still displayed on Cash Out page
        EXPECTED: The amount of cash out displayed on the button decreased accordingly by cashed out amount
        """
        wait_for_result(lambda: self.bet.buttons_panel.partial_cashout_button.is_displayed(),
                        timeout=5,
                        name='Confirmation text to disappear')

        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

        self.verify_user_balance(expected_user_balance=self.user_balance + self.partial_cashout_value)
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE,
                                                                              event_names=self.event_name,
                                                                              number_of_bets=1)
        self.assertTrue(bet, msg=f'Bet: "{self.bet_name}" not displayed after partial Cash Out')

        actual_cashout_value = self.bet.buttons_panel.full_cashout_button.amount.value
        expected_cashout_value = float(self.expected_cashout_value) - self.partial_cashout_value
        self.assertEqual(float(actual_cashout_value), expected_cashout_value,
                         msg=f'Actual cash out value: "{actual_cashout_value}", '
                             f'expected: "{expected_cashout_value}"')
