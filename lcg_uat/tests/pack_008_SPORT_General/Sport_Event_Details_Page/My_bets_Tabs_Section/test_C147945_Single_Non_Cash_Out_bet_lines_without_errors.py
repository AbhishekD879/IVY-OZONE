import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import generate_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.user_account
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.my_bets
@pytest.mark.currency
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.login
@vtest
class test_C147945_Single_Non_Cash_Out_bet_lines_without_errors(BaseCashOutTest):
    """
    TR_ID: C147945
    NAME: Single Non Cash Out bet lines without errors
    DESCRIPTION: This test case verifies single bet lines without errors on 'My bets' tab on Event Details page when the user is logged in.
    """
    keep_browser_open = True
    currency = '£'
    market_name = '|Market name %s|' % ' '.join([generate_name() for _ in range(10)])[:86]
    team1 = 'Auto test team one %s' % ' '.join([generate_name() for _ in range(7)])[:36]
    team2 = 'Auto test team two %s' % ' '.join([generate_name() for _ in range(7)])[:36]
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login to application
        DESCRIPTION: Place bet for test event
        """
        self.__class__.event_info = \
            self.ob_config.add_autotest_premier_league_football_event(cashout=False,
                                                                      default_market_name=self.market_name,
                                                                      team1=self.team1,
                                                                      team2=self.team2)
        self.__class__.event_name = f'{self.event_info.team1} v {self.event_info.team2}'
        self.__class__.selection_ids[self.event_info.team1] = self.event_info.selection_ids[self.event_info.team1]

        self.__class__.cashout_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - ' \
                                          f'[{self.event_info.team1}]'

        self.site.login()

        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.__class__.cashout_bet_info = self.place_and_validate_single_bet()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.event_info.event_id)
        if not self.site.sport_event_details.has_event_user_tabs_list(expected_result=False):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_verify_my_bets_tab(self):
        """
        DESCRIPTION: Verify 'My bets' tab
        EXPECTED: Bet sections are displayed for each bet
        EXPECTED: Separate section for each bet is present and includes following:
        EXPECTED: - Bet Section header
        EXPECTED: - Bet Section content with bet lines details
        """
        is_accordion_visible = wait_for_result(
            lambda: self.site.sport_event_details.my_bets.accordions_list.is_displayed(timeout=3),
            name='Accordion list to become visible')
        self.assertTrue(is_accordion_visible, msg='Accordion list with bet sections is not shown')

        self.__class__.event_groups_section = self.site.sport_event_details.my_bets.accordions_list
        self.__class__.bet_sections = self.event_groups_section.items_as_ordered_dict
        self.assertTrue(self.bet_sections, msg='No one bet section found on page')
        self.assertIn(self.cashout_bet_name, self.bet_sections.keys(),
                      msg=f'"{self.cashout_bet_name}" not found among: "{self.bet_sections.keys()}"')

        for bet_section_name, bet_section in self.bet_sections.items():
            self.assertTrue(bet_section.has_header(), msg=f'Bet: "{bet_section_name}" section header not found')

    def test_003_verify_bet_section_content_for_single_bet_without_available_cash_out(self):
        """
        DESCRIPTION: Verify Bet Section content for **Single ** bet without available cash out
        DESCRIPTION: Click/Tap Event Name
        EXPECTED: Single bet is displayed with the following information:
        EXPECTED: - Selection Name is displayed at the top of Bet Section
        EXPECTED: - Long name of a selection is fully displayed
        EXPECTED: - Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: - Market Name are displayed under Selection Name
        EXPECTED: - Market Name is wrapped to the next line if it is too long to be shown in one line
        EXPECTED: - Event Name is displayed under Market Name
        EXPECTED: - Event Name is wrapped to the next line if it is too long to be shown in one line
        EXPECTED: - Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/nth Set/ FT/Finished labels /"Watch live" icon (if available) can be displayed next to Event Name
        EXPECTED: - 'Stake' label with the relevant currency symbol, the monetary value is displayed under CAS OUT button on gray line (below divider - list view) (e.g. Stake £1.00)
        EXPECTED: - 'Est. Returns' label and the relevant currency symbol and amount are displayed on the same line as Stake (e.g. Est. Returns £1.00), where amount uses x,xxx,xxx.xx format
        EXPECTED: - Cash Out and Partial CashOut buttons are not shown under line with 'Stake' and 'Est. Returns'
        EXPECTED: Event Name is NOT clickable
        """
        bet_name, bet = self.event_groups_section.get_bet(event_names=self.event_info.team1, bet_type='SINGLE', number_of_bets=1)
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg found for bet: "{bet_name}"')

        for bet_leg_name, bet_leg in bet_legs.items():
            self.assertEqual(bet_leg.outcome_name, self.event_info.team1,
                             msg=f'Actual selection name: "{bet_leg.outcome_name}" not match '
                                 f'with expected: "{bet_leg.outcome_name}"')
            self.assertTrue(bet_leg.is_outcome_name_wrapped(), msg='Selection Name is not wrapped to the next line')

            expected_odd = self.ob_config.event.prices['odds_home']
            self.assertEqual(bet_leg.odds_value, expected_odd,
                             msg=f'Actual odd : "{bet_leg.odds_value}" not match with expected: "{expected_odd}"')

            self.__class__.market_name = self.market_name.replace('|', '').strip()
            self.assertEqual(bet_leg.market_name, self.market_name,
                             msg=f'Actual market name : "{bet_leg.market_name}" not match with '
                                 f'expected: "{self.market_name}"')
            self.assertTrue(bet_leg.is_market_name_wrapped(),
                            msg=f'Market Name "{self.market_name}" is not wrapped to the next line')
            self.assertEqual(bet_leg.event_name, self.event_name,
                             msg=f'Actual event name : "{bet_leg.event_name}" not match with '
                                 f'expected: "{self.event_name}"')
            self.assertTrue(bet_leg.is_event_name_wrapped(),
                            msg=f'Event Name "{self.event_name}" is not wrapped to the next line')
            self.compare_date_time(item_time_ui=bet_leg.event_time,
                                   event_date_time_ob=self.event_info.event_date_time,
                                   format_pattern='%H:%M, Today')

        expected_stake_amount = '{0}{1:.2f}'.format(self.currency, self.bet_amount)
        stake_amount = '{0}{1}'.format(bet.stake.currency, bet.stake.stake_value)
        self.assertEqual(stake_amount, expected_stake_amount,
                         msg=f'Actual stake amount: "{stake_amount}" not match with '
                             f'expected: "{expected_stake_amount}"')

        expected_est_returns = '{0}{1:.2f}'.format(self.currency,
                                                   self.cashout_bet_info[self.event_info.team1]['estimate_returns'])
        est_returns = '{0}{1}'.format(bet.est_returns.currency, bet.est_returns.stake_value)
        self.assertEqual(est_returns, expected_est_returns,
                         msg=f'Actual estimated returns amount: "{est_returns}" not match with '
                             f'expected: "{expected_est_returns}"')
        self.assertFalse(bet.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'CASHOUT button was found on bet: "{bet_name}" section')
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg=f'PARTIAL CASHOUT button was found on bet: "{bet_name}" section')

        bet_leg.click_event_name()
        current_tab_name = self.site.sport_event_details.event_user_tabs_list.current
        self.assertEqual(current_tab_name, self.my_bets_tab_name,
                         msg=f'"{self.my_bets_tab_name}" tab became inactive after event name click, '
                             f'current is: "{current_tab_name}"')

        edp_event_name = self.site.sport_event_details.event_title_bar.event_name
        expected_event_name = self.event_name.upper() if self.device_type == 'desktop' else self.event_name
        self.assertIn(edp_event_name, expected_event_name,
                      msg=f'Actual EDP name: "{edp_event_name}", expected: "{expected_event_name}"')
