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
class Test_C49399484_Verify_combination_error_message(Common):
    """
    TR_ID: C49399484
    NAME: Verify combination error message
    DESCRIPTION: This test case verifies error messages when combined markets/selections clash (cannot be combined).
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
    """
    keep_browser_open = True

    def test_001_clicktap_build_a_team_button___clicktap_plus_button_near_the_player_on_the_overlay___in_the_list_of_players_select_one_specific_that_cannot_be_combined_with_others(self):
        """
        DESCRIPTION: Click/tap 'Build a team' button -> click/tap '+' button near the player on the overlay -> in the list of players select one specific (that cannot be combined with others)
        EXPECTED: User is on Player Card View
        """
        pass

    def test_002_on_the_player_card_view_clicktap_add_player_button(self):
        """
        DESCRIPTION: On the Player Card view click/tap 'Add Player' button
        EXPECTED: - User is redirected to Pitch view
        EXPECTED: - An error message is displayed at the top of the pitch view and appears smoothly
        EXPECTED: - Message stays and does not disappear
        EXPECTED: - Error message informs what selections are incorrect (received in Network tab: 'price' request, 'responseMessage')
        EXPECTED: ![](index.php?/attachments/get/59483778)
        """
        pass

    def test_003_verify_the_pitch_view_overlay_when_this_error_occurs(self):
        """
        DESCRIPTION: Verify the pitch view overlay when this error occurs
        EXPECTED: - Only the players who are the incorrect combinations can be tapped on to edit
        EXPECTED: - The other players and positions are greyed out in inactive state
        EXPECTED: - 'Place Bet' button is not active
        """
        pass

    def test_004_edit_the_player_choose_one_that_is_already_taken_and_clicktap_add_player_button(self):
        """
        DESCRIPTION: Edit the player, choose one that is already taken and click/tap 'Add Player' button
        EXPECTED: - User is redirected to Pitch view
        EXPECTED: - An error message is displayed at the top of the pitch view
        EXPECTED: - Message stays and does not disappear
        EXPECTED: - Message informs that there are selections that cannot be combined in the team
        """
        pass

    def test_005_verify_the_pitch_view_overlay_when_this_error_occurs(self):
        """
        DESCRIPTION: Verify the pitch view overlay when this error occurs
        EXPECTED: - Only the players who are the duplicate selections can be tapped on to edit
        EXPECTED: - Other players and positions are greyed out in inactive state
        EXPECTED: - 'Place Bet' button is inactive
        """
        pass

    def test_006_edit_the_player_once_again_choosing_appropriate_selection_this_time_clicktap_add_player_button(self):
        """
        DESCRIPTION: Edit the player once again (choosing appropriate selection this time), click/tap 'Add Player' button
        EXPECTED: - User is redirected to Pitch view
        EXPECTED: - No error message is displayed anymore
        EXPECTED: - All player and position fields should become active again
        EXPECTED: - 'Place Bet' button should return to the active state
        """
        pass
