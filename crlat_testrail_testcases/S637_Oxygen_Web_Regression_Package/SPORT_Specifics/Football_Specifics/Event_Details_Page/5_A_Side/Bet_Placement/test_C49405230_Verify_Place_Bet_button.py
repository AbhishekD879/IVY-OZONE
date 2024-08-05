import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C49405230_Verify_Place_Bet_button(Common):
    """
    TR_ID: C49405230
    NAME: Verify 'Place Bet' button
    DESCRIPTION: This test case verifies 'Place Bet' button on pitch view overlay
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP:
    PRECONDITIONS: - '5 A Side' sub tab (event type described above):
    PRECONDITIONS: - 'Build a team' button (pitch view)
    """
    keep_browser_open = True

    def test_001_verify_the_button_state_when_no_players_are_selected_on_pitch_view(self):
        """
        DESCRIPTION: Verify the button state when no players are selected on pitch view
        EXPECTED: - 'Place Bet' button is in inactive state
        EXPECTED: - Odds are displayed as  '-/-'
        """
        pass

    def test_002_select_2_players_that_cannot_be_combined(self):
        """
        DESCRIPTION: Select 2 players that cannot be combined
        EXPECTED: - Error message is displayed at the top of pitch view
        EXPECTED: - 'Place Bet' button is in inactive state
        EXPECTED: - Odds are available
        EXPECTED: - All other positions ('+') are inactive
        EXPECTED: ![](index.php?/attachments/get/126095608)
        """
        pass

    def test_003_edit_players_and_select_2_valid_combinations(self):
        """
        DESCRIPTION: Edit players and select 2 valid combinations
        EXPECTED: - Odds are available on the left of the Place Bet' button
        EXPECTED: - Button becomes active
        EXPECTED: - All other positions ('+') are in active state
        EXPECTED: ![](index.php?/attachments/get/126095610)
        """
        pass

    def test_004_verify_price_request_pricenumpriceden_values_network_tab(self):
        """
        DESCRIPTION: Verify 'price' request: priceNum/priceDen values (Network tab)
        EXPECTED: priceNum/priceDen values are same as odds displayed on 'Place Bet' button
        """
        pass

    def test_005_clicktap_on_place_bet_button(self):
        """
        DESCRIPTION: Click/tap on 'Place Bet' button
        EXPECTED: - Bet builder is initiated
        """
        pass

    def test_006_go_back_to_pitch_view_and_select_all_5_players_valid_combinations(self):
        """
        DESCRIPTION: Go back to pitch view and select all 5 players (valid combinations)
        EXPECTED: - All players are selected
        EXPECTED: - Odds changes as the new players are added
        EXPECTED: - 'Place Bet' button becomes active and clickable
        """
        pass

    def test_007_unselect_some_of_the_players_on_condition_that_at_least_2_are_still_selected(self):
        """
        DESCRIPTION: Unselect some of the players (on condition that at least 2 are still selected)
        EXPECTED: - Odds changes as the players are unselected (can be found in 'price' request: priceNum/priceDen values)
        EXPECTED: - 'Place Bet' button is active and clickable
        """
        pass

    def test_008_unselect_all_players_except_1_selected(self):
        """
        DESCRIPTION: Unselect all players except 1 selected
        EXPECTED: - Only one player is selected the rest are displayed as '+'
        EXPECTED: - Odds changes accordingly
        EXPECTED: - 'Place Bet' button is inactive
        EXPECTED: ![](index.php?/attachments/get/126095612)
        """
        pass

    def test_009_change_the_formation_in_the_formation_carousel_and_then_go_back(self):
        """
        DESCRIPTION: Change the formation in the formation carousel and then go back
        EXPECTED: - All players are unselected
        EXPECTED: - 'Place Bet' button is inactive
        EXPECTED: - Odds are displayed as  '-/-'
        """
        pass

    def test_010_select_any_players_close_the_5_a_side_pitch_view_and_trigger_it_again_by_pressing_build_team_button(self):
        """
        DESCRIPTION: Select any players, close the 5 A Side pitch view and trigger it again (by pressing 'Build team' button)
        EXPECTED: - Pitch view is displayed cleared
        EXPECTED: - No players are selected
        EXPECTED: - 'Place Bet' button is inactive
        EXPECTED: - Odds are displayed as  '-/-'
        """
        pass

    def test_011_verify_edge_case_if_happensadd_1_player_and_observe_the_combination_error(self):
        """
        DESCRIPTION: Verify edge case (if happens):
        DESCRIPTION: Add 1 player and observe the combination error
        EXPECTED: - 'Place bet' button is disabled
        EXPECTED: - Error message is displayed
        EXPECTED: - priceNum: 0/priceDen: 0 is received in 'price' response
        EXPECTED: - All other '+' buttons are disabled as well
        EXPECTED: ![](index.php?/attachments/get/126095614)
        """
        pass
