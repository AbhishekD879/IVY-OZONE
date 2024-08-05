import pytest
import tests
import voltron.environments.constants as vec
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event can not be created in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28527_Verify_selection_data_and_placing_a_bet_on_Correct_Score_market(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28527
    NAME: Verify selection data and placing a bet on Correct Score market
    DESCRIPTION: This test case verifies selection data and bet placement on Correct Score market
    PRECONDITIONS: Football events with Correct Score market (name="Correct Score")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Jira ticket: **BMA-3861
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(markets=[('correct_score',
                                                                                    {'cashout': True})])
        self.__class__.market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.eventID = self.event.event_id
        self.__class__.event_name = '%s v %s' % (self.event.team1, self.event.team2)
        self.__class__.selection_name = "Draw 0-0"

        correct_score_prices = self.ob_config.event.correct_score_prices

        home_score_prices = correct_score_prices[0]
        sorted_home_score_prices = OrderedDict(sorted(home_score_prices[1].items()))
        self.__class__.home_prices = list(sorted_home_score_prices.values())

        away_score_prices = correct_score_prices[1]
        sorted_away_score_prices = OrderedDict(sorted(away_score_prices[1].items()))
        self.__class__.away_prices = list(sorted_away_score_prices.values())

        draw_score_prices = correct_score_prices[2]
        sorted_draw_score_prices = OrderedDict(sorted(draw_score_prices[1].items()))
        self.__class__.draw_prices = list(sorted_draw_score_prices.values())

        expected_goals = []
        for result in correct_score_prices:
            for score in list(result[1].keys()):
                expected_goals.append(score[0])
        self.__class__.expected_goals_quantity = sorted(list(set(expected_goals)))

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.login(user=tests.settings.default_username)
        self.__class__.balance = self.site.header.user_balance
        self.site.wait_content_state('Homepage')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_correct_score_market_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' market section
        EXPECTED: *   Section is present on Event Details Page
        EXPECTED: *   It is possible to collapse/expand section
        """
        self.__class__.market_name = self.expected_market_sections.correct_score
        self.assertIn(self.market_name, self.markets_list, msg=f'"{self.market_name}" section is not present')

        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{self.market_name}" section is not found in "{self.markets_list.keys()}"')
        self.correct_score.collapse()
        self.assertFalse(self.correct_score.is_expanded(expected_result=False),
                         msg=f'"{self.market_name}" section is not collapsed')

        self.correct_score.expand()
        self.assertTrue(self.correct_score.is_expanded(),
                        msg=f'"{self.market_name}" section is not expanded')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: All selections are displayed on 'Show All' section:
        EXPECTED: *   outcomes names correspond to the SS attribute 'name's for appropriate 'outcome ID'
        EXPECTED: *   Price/odds buttons
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown as N/A
        EXPECTED: * Any other selection without scores and with Price/Odds should be available.
        """
        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')
        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')

        home_actual_prices = self.correct_score.outcome_table.home_outcomes.outcomes_prices
        self.assertEquals(self.home_prices, home_actual_prices,
                          msg=f'Expected prices for home team: "{self.home_prices}"'
                              f' are not equal to actual: "{home_actual_prices}"')

        draw_actual_prices = self.correct_score.outcome_table.draw_outcomes.outcomes_prices
        self.assertEquals(self.draw_prices, draw_actual_prices,
                          msg=f'Expected prices for home team: "{self.draw_prices}"'
                              f' are not equal to actual: "{draw_actual_prices}"')

        away_actual_prices = self.correct_score.outcome_table.away_outcomes.outcomes_prices
        self.assertEquals(self.away_prices, away_actual_prices,
                          msg=f'Expected prices for home team: "{self.away_prices}"'
                              f' are not equal to actual: "{away_actual_prices}"')

    def test_005_verify_data_of_priceodds_button_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen
        """

        self.assertTrue(self.correct_score.team_home_scores, msg='Home team result drop-down is not present')
        self.assertTrue(self.correct_score.team_away_scores, msg='Away team result drop-down is not present')

        self.assertEquals(self.correct_score.team_home_scores.selected_item, '0',
                          msg='Default value for home team result drop-down is not "0"')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '0',
                          msg='Default value for away team result drop-down is not "0"')

        self.assertEquals(self.correct_score.combined_outcome_button.name, self.draw_prices[0],
                          msg=f'Outcome price "{self.correct_score.combined_outcome_button.name}" '
                              f'is not the same as expected "{self.draw_prices[0]}" in case of invalid result selection')
        self.assertRegexpMatches(self.correct_score.combined_outcome_button.name, self.fractional_pattern,
                                 msg=f'Selection odds value "{self.correct_score.combined_outcome_button.name}" not match '
                                     f'decimal pattern: "{self.fractional_pattern}"')

    def test_006_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')
        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{self.market_name}" section is not found in "{self.markets_list.keys()}"')
        self.assertRegexpMatches(self.correct_score.combined_outcome_button.name, self.decimal_pattern,
                                 msg=f'Selection odds value "{self.correct_score.combined_outcome_button.name}" not match '
                                     f'decimal pattern: "{self.decimal_pattern}"')

    def test_007_tap_on_default_add_to_betslip_priceodds_button(self):
        """
        DESCRIPTION: Tap on default 'Add to Betslip <price/odds>' button
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted on 'Show All' section automatically
        EXPECTED: *   If price is not available - Add to Betslip button become N/A
        """
        self.correct_score.add_to_betslip_button.click()
        self.assertTrue(self.correct_score.add_to_betslip_button.is_selected(),
                        msg='Outcome button is not highlighted in green')
        if self.device_type == "mobile":
            quick_bet = self.site.quick_bet_panel
            self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                             msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet is not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

        self.verify_betslip_counter_change(expected_value=1)
        self.site.open_betslip()
        self.assertEqual(self.correct_score.add_to_betslip_button.background_color_value,
                         vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Selected price/odds for "{self.correct_score.add_to_betslip_button.name}"'
                             f' background color "{self.correct_score.add_to_betslip_button.background_color_value}" '
                             f'is not highlighted in green {vec.colors.SELECTED_BET_BUTTON_COLOR}')

    def test_008_tap_add_to_betslip_priceodds_button_again(self):
        """
        DESCRIPTION: Tap 'Add to Betslip <price/odds>' button again
        EXPECTED: *   Bet indicator disappeared
        EXPECTED: *   Outcome on 'Show All' section is unhighlighted respectively
        """
        self.site.close_betslip()
        self.correct_score.add_to_betslip_button.click()
        self.assertNotEqual(self.correct_score.add_to_betslip_button.background_color_value,
                            vec.colors.SELECTED_BET_BUTTON_COLOR)

    def test_009_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: *   Bet indicator displays 1
        EXPECTED: *   Outcome is green highlighted on 'Show All' section automatically
        """
        self.correct_score.add_to_betslip_button.click()
        if self.device_type == "mobile":
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)
        self.site.open_betslip()
        self.assertEqual(self.correct_score.add_to_betslip_button.background_color_value,
                         vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Selected price/odds for "{self.correct_score.add_to_betslip_button.name}"'
                             f' background color "{self.correct_score.add_to_betslip_button.background_color_value}" '
                             f'is not highlighted in green {vec.colors.SELECTED_BET_BUTTON_COLOR}')

    def test_010_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to 'Bet Slip'
        EXPECTED: The bet is present
        """
        self.__class__.singles_section = self.get_betslip_sections().Singles
        bet_name, self.__class__.bet = list(self.singles_section.items())[0]
        self.assertEqual(bet_name, self.selection_name,
                         msg=f'Actual: "{bet_name}" bet name is not matched with Expected: Draw 0-0')

    def test_011_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fractional format or **'price Dec'** in decimal format)
        """

        self.__class__.stake = self.singles_section.get("Draw 0-0")
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found')
        event_name = self.stake.event_name
        self.assertEqual(event_name, f"{self.event.team1} v {self.event.team2}",
                         msg=f'Selection name "{event_name}" is not the same as expected {self.event.team1} v {self.event.team2}')
        outcome_name = self.stake.outcome_name
        self.assertEqual(outcome_name, self.selection_name,
                         msg=f'Selection name "{outcome_name}" is not the same as expected "{self.selection_name}"')
        if self.device_type == 'mobile' and self.brand == 'bma':
            market_name = self.stake.market_name.upper()
        else:
            market_name = self.stake.market_name

        self.assertEqual(market_name, self.market_name,
                         msg=f'Market name "{market_name}" is not the same as expected "{self.market_name}"')

    def test_012_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Est. Returns**(Coral)/ **Pot. Returns** (Ladbrokes)
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Estimated Returns**(Coral)/ **Potential Returns** (Ladbrokes)
        """
        self.place_single_bet(number_of_stakes=1)

    def test_013_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)
