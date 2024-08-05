import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


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
@pytest.mark.cash_out
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-56339')
@vtest
class Test_C147946_Multiple_Cash_Out_bet_lines_without_errors(BaseCashOutTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C147946
    VOL_ID: C9698014
    NAME: Multiple Cash Out bet lines without errors
    """
    keep_browser_open = True
    currency = '£'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Test events created
        """
        self.__class__.sport_event_info = self.ob_config.add_tennis_event_to_autotest_trophy(cashout=True)
        self.__class__.sport_event_name = f'{self.sport_event_info.team1} v {self.sport_event_info.team2}'
        self.__class__.selection_ids[self.sport_event_info.team1] = \
            self.sport_event_info.selection_ids[self.sport_event_info.team1]
        self.__class__.racing_event_info = self.ob_config.add_UK_racing_event(cashout=True, number_of_runners=1,
                                                                              ew_terms=self.ew_terms)
        self.__class__.racing_selection_name = list(self.racing_event_info.selection_ids.keys())[0]
        self.__class__.racing_event_name = f'{self.racing_event_info.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.selection_ids.update(self.racing_event_info.selection_ids)

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_place_bet_for_events(self):
        """
        DESCRIPTION: Place bet for test events
        """
        # Adding each selection separately to know exact order of bet legs
        self.navigate_to_edp(event_id=self.sport_event_info.event_id)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.sport_event_info.team1,
                                                           market_name=self.expected_market_sections.match_betting)

        quick_bet = self.site.quick_bet_panel
        quick_bet.add_to_betslip_button.click()

        self.verify_betslip_counter_change(expected_value=1)

        self.navigate_to_edp(event_id=self.racing_event_info.event_id, sport_name='horse-racing')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')

        outcome = outcomes.get(self.racing_selection_name)
        self.assertTrue(outcome, msg=f'Outcome "{self.racing_selection_name}" not found')
        outcome.bet_button.click()

        self.verify_betslip_counter_change(expected_value=2)

        self.site.open_betslip()
        self.__class__.bet_info = self.place_and_validate_multiple_bet()
        self.check_bet_receipt_is_displayed()

        self.site.bet_receipt.footer.click_done()
        self.site.has_betslip_opened(expected_result=False)

    def test_003_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.sport_event_info.event_id)
        if not self.site.sport_event_details.has_event_user_tabs_list(expected_result=False):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_004_verify_my_bets_tab(self):
        """
        DESCRIPTION: Verify 'My bets' tab
        EXPECTED: Bet sections are displayed for each bet
        EXPECTED: Separate section for each bet is present and includes following:
        EXPECTED: - Bet Section header
        EXPECTED: - Bet Section content with bet lines details
        """
        self.site.sport_event_details.my_bets.accordions_list.verify_cashout_bet_layout_elements(number_of_events=2)
        self.__class__.bet_sections = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertTrue(self.bet_sections, msg='No one bet section found on page')
        for bet_section_name, bet_section in self.bet_sections.items():
            self.assertTrue(bet_section.has_header(), msg=f'Bet: "{bet_section_name}" section header not found')

    def test_005_verify_sport_bet_section_content(self):
        """
        DESCRIPTION: Verify Tennis Bet Section content for Multiple bet
        EXPECTED: Selection Name is displayed at the top of Bet Section
        EXPECTED: Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: Market Name is displayed under Selection Name
        EXPECTED: Event Name is displayed under Market Name
        EXPECTED: Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/nth Set/FT/Finished labels / "Watch live" icon (if available) can be displayed next to Event Name
        """
        self.__class__.event_groups_section = \
            self.site.sport_event_details.my_bets.accordions_list
        self.__class__.bet_name, self.__class__.bet = \
            self.event_groups_section.get_bet(event_names=[self.sport_event_info.team1,
                                                           self.racing_selection_name],
                                              bet_type='DOUBLE',
                                              number_of_bets=2)
        self.__class__.bet_legs = self.bet.items_as_ordered_dict
        self.assertTrue(self.bet_legs, msg=f'No one bet leg found for bet: "{self.sport_event_name}"')
        self.assertIn(self.sport_event_info.team1, self.bet_legs.keys())
        self.__class__.sport_bet_leg = self.bet_legs[self.sport_event_info.team1]
        self.assertEqual(self.sport_bet_leg.outcome_name, self.sport_event_info.team1,
                         msg='Actual selection name: "%s" not match with expected: "%s"'
                             % (self.sport_bet_leg.outcome_name, self.sport_event_info.team1))
        expected_odd = self.ob_config.event.prices['odds_home']
        self.assertEqual(self.sport_bet_leg.odds_value, expected_odd,
                         msg='Actual odd : "%s" not match with expected: "%s"'
                             % (self.sport_bet_leg.odds_value, expected_odd))
        expected_market_name = self.ob_config.tennis_config.tennis_autotest.autotest_trophy.market_name.replace('|', '')
        self.assertEqual(self.sport_bet_leg.market_name, expected_market_name,
                         msg='Actual market name : "%s" not match with expected: "%s"'
                             % (self.sport_bet_leg.market_name, expected_market_name))
        self.assertEqual(self.sport_bet_leg.event_name, self.sport_event_name,
                         msg='Actual event name : "%s" not match with expected: "%s"'
                             % (self.sport_bet_leg.event_name, self.sport_event_name))
        self.compare_date_time(item_time_ui=self.sport_bet_leg.event_time,
                               event_date_time_ob=self.sport_event_info.event_date_time,
                               format_pattern='%H:%M, Today')
        self.sport_bet_leg.scroll_to()
        self.sport_bet_leg.click_event_name()
        current_tab_name = self.site.sport_event_details.event_user_tabs_list.current
        self.assertEqual(current_tab_name, self.my_bets_tab_name,
                         msg='My Bets tab became inactive after event name click, current is: "%s"'
                             % current_tab_name)
        edp_event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(edp_event_name, self.sport_event_name,
                         msg='Bet event name is clickable, actual EDP name: "%s", expected: "%s"'
                             % (edp_event_name, self.sport_event_name))

    def test_006_verify_racing_bet_section_content(self):
        """
        DESCRIPTION: Verify Racing Bet Section content for Multiple bet
        EXPECTED: Selection Name is displayed at the top of Bet Section
        EXPECTED: Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: Market Name is displayed under Selection Name
        EXPECTED: Event Name is displayed under Market Name
        EXPECTED: Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/nth Set/FT/Finished labels / "Watch live" icon (if available) can be displayed next to Event Name
        """
        self.assertIn(self.racing_selection_name, self.bet_legs.keys())
        self.__class__.racing_bet_leg = self.bet_legs[self.racing_selection_name]
        self.assertEqual(self.racing_bet_leg.outcome_name, self.racing_selection_name,
                         msg='Actual selection name: "%s" not match with expected: "%s"'
                             % (self.racing_bet_leg.outcome_name, self.racing_selection_name))
        self.assertEqual(self.racing_bet_leg.odds_value, 'SP',
                         msg='Actual odd : "%s" not match with expected: "SP"'
                             % self.racing_bet_leg.odds_value)
        expected_market_name = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.market_name.replace('|', '')
        self.assertEqual(self.racing_bet_leg.market_name, expected_market_name,
                         msg='Actual market name : "%s" not match with expected: "%s"'
                             % (self.racing_bet_leg.market_name, expected_market_name))
        self.assertEqual(self.racing_bet_leg.event_name, self.racing_event_name,
                         msg='Actual event name : "%s" not match with expected: "%s"'
                             % (self.racing_bet_leg.event_name, self.racing_event_name))
        self.compare_date_time(item_time_ui=self.racing_bet_leg.event_time,
                               event_date_time_ob=self.racing_event_info.event_date_time,
                               format_pattern='%H:%M, Today')

    def test_007_verify_bet_receipt_section_and_buttons_panel(self):
        """
        DESCRIPTION: Verify bet receipt section and buttons panel
        EXPECTED: 'Stake' label with the relevant currency symbol and the monetary value is displayed (e.g. Stake £1.00), where stake uses x,xxx,xxx.xx format
        EXPECTED: 'Est. Returns' label and the relevant currency symbol and amount are displayed on the same line as Stake (e.g. Est. Returns £1.00), where amount uses x,xxx,xxx.xx format
        EXPECTED: Button with label "CASH OUT: <currency symbol><amount>" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button (on area without "PARTIAL CASHOUT" section)
        EXPECTED: Button with label "PARTIAL CASHOUT" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button
        EXPECTED: Slider for selecting the sum of partial cashout is displayed instead of Cash Out button after clicking on 'PARTIAL CASHOUT' button. By default for each bet the slider is at 50%. The sum which equals to 10% of the full cahout is the lowest point for the slider. Highest point is full cashout value
        """
        expected_stake_amount = '{0}{1:.2f}'.format(self.currency, self.bet_amount)
        stake_amount = '{0}{1}'.format(self.bet.stake.currency, self.bet.stake.stake_value)
        self.assertEqual(stake_amount, expected_stake_amount,
                         msg='Actual stake amount: "%s" not match with expected: "%s"'
                             % (stake_amount, expected_stake_amount))
        expected_est_returns = 'N/A'
        self.assertEqual(self.bet.est_returns.value, expected_est_returns,
                         msg='Actual estimated returns amount: "%s" not match with expected: "%s"'
                             % (self.bet.est_returns.value, expected_est_returns))
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(),
                        msg='CASHOUT button was not found on bet: "%s" section' % self.bet_name)
        self.assertEqual(self.bet.buttons_panel.full_cashout_button.label, 'CASH OUT')
        cashout_button_amount = self.bet.buttons_panel.full_cashout_button.amount
        cashout_value = '{0}{1}'.format(cashout_button_amount.currency, cashout_button_amount.value)
        expected_cashout_amount = self.bet_amount - (self.bet_amount * 0.1)
        expected_cashout_value = '{0}{1:.2f}'.format(self.currency, expected_cashout_amount)
        self.assertEqual(cashout_value, expected_cashout_value,
                         msg='Actual Cash Out button value: "%s" not match with expected: "%s"'
                             % (cashout_value, expected_cashout_value))

        # Partial CashOut shouldn't be executed
        # self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
        #                 msg='PARTIAL CASHOUT button was not found on bet: "%s" section' % self.bet_name)
        # self.bet.buttons_panel.partial_cashout_button.click()
        # self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), 'PARTIAL CASHOUT slider was not appeared')
        #
        # expected_partial_cashout_amount = '{0:.2f}'.format(expected_cashout_amount * 0.5)
        # wait_for_result(lambda: expected_partial_cashout_amount in self.bet.buttons_panel.partial_cashout_button.amount.value,
        #                 timeout=1,
        #                 name='Expected partial cashout timeout to appear')
        # partial_cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        # self.assertEqual(partial_cashout_amount, expected_partial_cashout_amount,
        #                  msg=f'Actual default partial cash out amount: "{partial_cashout_amount}", '
        #                      f'expected: "{expected_partial_cashout_amount}"')

    def test_008_click_on_racing_event_name(self):
        """
        DESCRIPTION: Click on Racing event name
        EXPECTED: Event Details page is opened for corresponding event from Multiple bet after click on event name
        """
        self.racing_bet_leg.click_event_name()
        self.site.wait_content_state('RacingEventDetails')

        breadcrumbs = self.site.racing_event_details.breadcrumbs.items_as_ordered_dict
        self.assertIn(self.horseracing_autotest_uk_name_pattern, breadcrumbs,
                      msg=f'Bet event name is not clickable, actual EDP names: "{breadcrumbs}", '
                          f'expected: "{self.horseracing_autotest_uk_name_pattern}"')

        selected_event = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        self.assertEqual(selected_event, self.racing_event_info.event_off_time,
                         msg=f'Wrong EDP opened. Opened for: "{selected_event}", '
                             f'expected was: "{self.racing_event_info.event_off_time}"')
