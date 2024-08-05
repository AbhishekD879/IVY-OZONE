import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.scorecast
@pytest.mark.event_details
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.pipelines
@pytest.mark.login
@vtest
class Test_C1033082_Verify_Bet_Placement_on_Scorecast_Selection(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C1033082
    VOL_ID: C9697744
    NAME: Verify Bet Placement on Scorecast Selection
    DESCRIPTION: This test case verifies Bet Placement on Scorecast Selection
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True
    team_result = '1'
    market = 'First Goalscorer, Correct Score'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with Scorecast and navigate to it event details page
        """
        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('scorecast', {'cashout': True})])
        self.__class__.created_event_name = self.event_params.team1 + ' v ' + self.event_params.team2
        self.navigate_to_edp(event_id=self.event_params.event_id)

    def test_001_log_in_to_oxygen(self):
        """
        DESCRIPTION: Log in to Oxygen application, get user balance
        """
        self.site.login(async_close_dialogs=False)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_select_first_player_to_score_last_player_to_score_and_correct_score(self):
        """
        DESCRIPTION:  Select First Player to Score / Last Player to Score and Correct Score
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        keys = ' ,'.join(markets.keys())
        self.assertIn(self.expected_market_sections.scorecast, markets,
                      msg=f'"{self.expected_market_sections.scorecast}" market was not found in list of markets "{keys}"')
        self.__class__.scorecast = markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(self.scorecast, msg='SCORECAST section is not found')
        self.scorecast.expand()

        self.scorecast.home_team_results_dropdown.select_value(self.team_result)
        self.scorecast.away_team_results_dropdown.select_value(self.team_result)
        self.scorecast.player_scorers_list.select_player_by_index(index=2)
        player = self.scorecast.player_scorers_list.selected_item

        self.__class__.expected_outcome_name = f'{player}, Draw {self.team_result}-{self.team_result}'
        self.__class__.output_price = self.scorecast.output_price
        self._logger.debug(f'*** Output price for player "{player}" is: "{self.output_price}"')
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(),
                        msg='"Odds calculation" button is not active')

    def test_003_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: 'Odds calculation' button is selected and highlighted in green
        """
        self.scorecast.add_to_betslip.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        self.assertTrue(self.scorecast.add_to_betslip.is_selected(),
                        msg='"Odds calculation" button is not highlighted in green')

    def test_004_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        quick_bet = self.site.quick_bet_panel.selection
        quick_bet.content.amount_form.input.value = self.bet_amount
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: Bet Receipt is displayed with bet ID number
        EXPECTED: Bet is placed successfully
        EXPECTED: User balance is decreased by stake entered on step #4
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()

        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertTrue(self.bet_receipt.bet_id, msg='Bet ID is not shown on Bet Receipt')

        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance, delta=0.03)

    def test_006_verify_selection_name_correctness(self):
        """
        DESCRIPTION: Verify Selection name correctness
        EXPECTED: Selection name consists of two parts: Name 1, Name 2, where:
        EXPECTED: - Name 1 corresponds to receipt.outcome.name
        EXPECTED: - Name 2 corresponds to receipt.legParts.[i].outcomeDesc when marketDesc = Correct Score
        """
        self.assertEqual(self.bet_receipt.name, self.expected_outcome_name,
                         msg=f'Actual Outcome Name "{self.bet_receipt.name}" does not match expected "{self.expected_outcome_name}"')
        self.assertEqual(self.bet_receipt.event_market, self.market,
                         msg=f'Actual Market Name "{self.bet_receipt.event_market}" does not match expected "{self.market}"')
        self.assertEqual(self.bet_receipt.event_name, self.created_event_name,
                         msg=f'Actual Event Name "{self.bet_receipt.event_name}" does not match expected "{self.created_event_name}"')
        self.assertEqual(self.bet_receipt.odds, self.output_price,
                         msg=f'Actual odds "{self.bet_receipt.odds}" does not match expected "{self.output_price}"')
