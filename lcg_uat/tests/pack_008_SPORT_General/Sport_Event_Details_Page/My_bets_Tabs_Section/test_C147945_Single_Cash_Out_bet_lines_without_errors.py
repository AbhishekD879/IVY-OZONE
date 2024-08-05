import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.user_journey_football_multiple
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
class test_C147945_Single_Cash_Out_bet_lines_without_errors(BaseCashOutTest):
    """
    TR_ID: C147945
    NAME: Single Cash Out bet lines without errors
    DESCRIPTION: This test case verifies single bet lines without errors on 'My bets' tab on Event Details page when the user is logged in.
    """
    keep_browser_open = True
    currency = '£'
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        self.__class__.event_info = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name = '%s v %s' % (self.event_info.team1, self.event_info.team2)
        self.__class__.selection_ids[self.event_info.team1] = self.event_info.selection_ids[self.event_info.team1]
        self.__class__.cashout_bet_name = 'SINGLE - [%s]' % self.event_info.team1

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_place_bet_for_events(self):
        """
        DESCRIPTION: Place bet for test event
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.__class__.cashout_bet_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.event_info.event_id, sport_name='football')
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_004_verify_my_bets_tab(self):
        """
        DESCRIPTION: Verify 'My bets' tab
        EXPECTED: Bet sections are displayed for each bet
        EXPECTED: Separate section for each bet is present and includes following:
        EXPECTED: - Bet Section header
        EXPECTED: - Bet Section content with bet lines details
        """
        self.__class__.event_groups_section = self.site.sport_event_details.my_bets.accordions_list
        self.event_groups_section.verify_cashout_bet_layout_elements(number_of_events=1)
        self.__class__.bet_sections = self.event_groups_section.items_as_ordered_dict
        self.assertTrue(self.bet_sections, msg='No one bet section found on page')
        self.assertIn(self.cashout_bet_name, self.bet_sections.keys())
        for bet_section_name, bet_section in self.bet_sections.items():
            self.assertTrue(bet_section.has_header(), msg=f'Bet: "{bet_section_name}" section header not found')

    def test_005_verify_bet_section_content_for_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Verify Bet Section content for **Single ** bet with available cash out
        DESCRIPTION: Click/Tap Event Name
        EXPECTED: Single bet is displayed with the following information:
        EXPECTED: - Selection Name is displayed at the top of Bet Section
        EXPECTED: - Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: - Market Name are displayed under Selection Name
        EXPECTED: - Event Name is displayed under Market Name
        EXPECTED: - Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/nth Set/ FT/Finished labels /"Watch live" icon (if available) can be displayed next to Event Name
        EXPECTED: - 'Stake' label with the relevant currency symbol, the monetary value is displayed under CASH OUT button on gray line (below divider - list view) (e.g. Stake £1.00)
        EXPECTED: - 'Est. Returns' label and the relevant currency symbol and amount are displayed on the same line as Stake (e.g. Est. Returns £1.00), where amount uses x,xxx,xxx.xx format
        EXPECTED: - Button with label "CASH OUT: <currency symbol><amount>" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button (on area without "PARTIAL CASHOUT" section)
        EXPECTED: - Button with label "PARTIAL CASHOUT" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button
        EXPECTED: - Slider for selecting the sum of partial cashout ' is displayed instead of Cash Out button after clicking on 'PARTIAL CASHOUT' button.
        EXPECTED: - By default for each bet the slider is at 50%
        EXPECTED: Event Name is NOT clickable
        """
        bet_name, bet = self.event_groups_section.get_bet(event_names=self.event_info.team1, bet_type='SINGLE', number_of_bets=1)
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg found for bet: "{self.event_name}"')
        for bet_leg_name, bet_leg in bet_legs.items():
            self.assertEqual(bet_leg.outcome_name, self.event_info.team1,
                             msg='Actual selection name: "%s" not match with expected: "%s"'
                                 % (bet_leg.outcome_name, self.event_info.team1))
            expected_odd = self.ob_config.event.prices['odds_home']
            self.assertEqual(bet_leg.odds_value, expected_odd,
                             msg='Actual odd : "%s" not match with expected: "%s"'
                                 % (bet_leg.odds_value, expected_odd))
            expected_market_name = self.ob_config.football_config.autotest_class.\
                autotest_premier_league.market_name.replace('|', '')
            self.assertEqual(bet_leg.market_name, expected_market_name,
                             msg='Actual market name : "%s" not match with expected: "%s"'
                                 % (bet_leg.market_name, expected_market_name))
            self.assertEqual(bet_leg.event_name, self.event_name,
                             msg='Actual event name : "%s" not match with expected: "%s"'
                                 % (bet_leg.event_name, self.event_name))
            self.compare_date_time(item_time_ui=bet_leg.event_time,
                                   event_date_time_ob=self.event_info.event_date_time,
                                   format_pattern='%H:%M, Today')
        expected_stake_amount = '{0}{1:.2f}'.format(self.currency, self.bet_amount)
        stake_amount = '{0}{1}'.format(bet.stake.currency, bet.stake.stake_value)
        self.assertEqual(stake_amount, expected_stake_amount,
                         msg='Actual stake amount: "%s" not match with expected: "%s"'
                             % (stake_amount, expected_stake_amount))
        expected_est_returns = '{0}{1:.2f}'.format(self.currency,
                                                   self.cashout_bet_info[self.event_info.team1]['estimate_returns'])
        est_returns = '{0}{1}'.format(bet.est_returns.currency, bet.est_returns.stake_value)
        self.assertEqual(est_returns, expected_est_returns,
                         msg='Actual estimated returns amount: "%s" not match with expected: "%s"'
                             % (est_returns, expected_est_returns))
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(),
                        msg='CASHOUT button was not found on bet: "%s" section' % bet_name)
        self.assertEqual(bet.buttons_panel.full_cashout_button.label, 'CASH OUT')
        cashout_button_amount = bet.buttons_panel.full_cashout_button.amount
        cashout_value = '{0}{1}'.format(cashout_button_amount.currency, cashout_button_amount.value)
        expected_cashout_amount = self.bet_amount - (self.bet_amount * 0.1)
        expected_cashout_value = '{0}{1:.2f}'.format(self.currency, expected_cashout_amount)
        self.assertEqual(cashout_value, expected_cashout_value,
                         msg='Actual Cash Out button value: "%s" not match with expected: "%s"'
                             % (cashout_value, expected_cashout_value))
        # Partial CashOut shouldn't be executed
        # self.assertTrue(bet.buttons_panel.has_partial_cashout_button(),
        #                 msg='PARTIAL CASHOUT button was not found on bet: "%s" section' % bet_name)
        # bet.buttons_panel.partial_cashout_button.click()
        # self.assertTrue(bet.buttons_panel.wait_for_cashout_slider(), 'PARTIAL CASHOUT slider was not appeared')
        # expected_partial_cashout_amount = '{0:.2f}'.format(expected_cashout_amount * 0.5)
        # wait_for_result(lambda: bet.buttons_panel.partial_cashout_button.amount.value == expected_partial_cashout_amount,
        #                 name='Partial cashout value changes',
        #                 timeout=1)
        # partial_cashout_amount = bet.buttons_panel.partial_cashout_button.amount.value
        #
        # self.assertEqual(partial_cashout_amount, expected_partial_cashout_amount,
        #                  msg='Actual default partial cash out amount: "%s", expected: "%s"'
        #                      % (partial_cashout_amount, expected_partial_cashout_amount))
        # bet_leg.click_event_name()
        # current_tab_name = self.site.sport_event_details.event_user_tabs_list.current
        # self.assertEqual(current_tab_name, self.my_bets_tab_name,
        #                  msg='"%s" tab became inactive after event name click, current is: "%s"'
        #                      % (self.my_bets_tab_name, current_tab_name))
        #
        # edp_event_name = self.site.sport_event_details.event_title_bar.event_name
        # expected_event_name = self.event_name.upper() if self.device_type == 'desktop' else self.event_name
        # self.assertEqual(edp_event_name, expected_event_name,
        #                  msg='Bet event name is clickable, actual EDP name: "%s", expected: "%s"'
        #                      % (edp_event_name, expected_event_name))
