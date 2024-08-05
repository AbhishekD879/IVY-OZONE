import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.quick_bet
@pytest.mark.scorecast
@pytest.mark.mobile_only
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@vtest
class Test_C1033081_Verify_Adding_Scorecast_Selection_to_Quick_bet(BaseSportTest):
    """
    TR_ID: C1033081
    VOL_ID: C9697782
    NAME: Verify Adding Scorecast Selection to Quick bet
    DESCRIPTION: This test case verifies adding Scorecast selection to Quick bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    """
    keep_browser_open = True
    team_result = '1'
    market = 'First Goal Scorecast'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event.event_id
        self.__class__.created_event_name = event.team1 + ' v ' + event.team2

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_select_first_player_to_score_last_player_to_score_and_correct_score(self):
        """
        DESCRIPTION: Select **First Player to Score** / **Last Player to Score** and **Correct Score**
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        self.assertIn(self.expected_market_sections.scorecast, markets, msg='SCORECAST market was not found in "%s"' % markets)
        scorecast = markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(scorecast, msg='SCORECAST section is not found')
        scorecast.expand()
        is_market_section_expanded = scorecast.is_expanded()
        self.assertTrue(is_market_section_expanded, msg='SCORECAST market is not expanded')

        scorecast.home_team_results_dropdown.select_value(self.team_result)
        scorecast.away_team_results_dropdown.select_value(self.team_result)
        scorecast.player_scorers_list.select_player_by_index(index=2)
        player = scorecast.player_scorers_list.selected_item

        self.__class__.expected_outcome_name = f'{player}, Draw {self.team_result}-{self.team_result}'
        output_price = scorecast.output_price
        self._logger.debug(f'*** Output price for player "{player}" is: "{output_price}"')

        self.assertTrue(scorecast.add_to_betslip.is_enabled(timeout=10), msg='Odds button is not active')
        scorecast.add_to_betslip.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_003_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        DESCRIPTION: Verify Market Name
        EXPECTED: Selection Name consists of two part:
        EXPECTED: Name 1,  Name 2,
        EXPECTED: where
        EXPECTED: Name 1 corresponds to **event.markets.[i].outcome.name**
        EXPECTED: and Name 2 corresponds to **event.market.[i+1].outcome.name** from 51001 response in WS
        EXPECTED: **NOTE** that selection part from Correct Score market should be always displayed in the second place
        EXPECTED: Market Name corresponds to **event.markets.[i].name** attribute from 51001 response in WS
        EXPECTED: where i - the number of markets returned in response
        EXPECTED: **NOTE** possible market names : **First Player to Score** , **Last Player to Score**
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        self.assertEqual(quick_bet.event_name, self.created_event_name,
                         msg='Actual Event Name "%s" does not match expected "%s"' %
                             (quick_bet.event_name, self.created_event_name))
        self.assertEqual(quick_bet.market_name, self.market,
                         msg='Actual Market Name "%s" does not match expected "%s"' %
                             (quick_bet.market_name, self.market))
        self.assertEqual(quick_bet.outcome_name, self.expected_outcome_name,
                         msg='Actual Outcome Name "%s" does not match expected "%s"' %
                             (quick_bet.outcome_name, self.expected_outcome_name))
