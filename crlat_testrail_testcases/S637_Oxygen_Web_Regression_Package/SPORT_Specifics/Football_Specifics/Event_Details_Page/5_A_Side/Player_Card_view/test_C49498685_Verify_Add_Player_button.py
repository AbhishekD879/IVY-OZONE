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
class Test_C49498685_Verify_Add_Player_button(Common):
    """
    TR_ID: C49498685
    NAME: Verify 'Add Player' button
    DESCRIPTION: This test case verifies 'Add Player' button on player card overlay
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: OX 103 design changes:
    PRECONDITIONS: https://zpl.io/V4xq3W0
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP: Player Card view
    PRECONDITIONS: - '5 A Side' sub tab (event type described above):
    """
    keep_browser_open = True

    def test_001_clicktap_build_a_team_button___clicktap_plus_button_near_the_player_on_the_overlay___in_the_list_of_players_select_one_specific(self):
        """
        DESCRIPTION: Click/tap 'Build a team' button -> click/tap '+' button near the player on the overlay -> in the list of players select one specific
        EXPECTED: User is on Player Card View
        """
        pass

    def test_002_verify_the_button_state_before_user_changes_the_stats_value(self):
        """
        DESCRIPTION: Verify the button state before user changes the stats value
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - Odds are displayed
        EXPECTED: ![](index.php?/attachments/get/60279451)
        EXPECTED: OX 103:
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - 'Add Player' button is visually separated from odds with lighter color
        EXPECTED: - 'ODDS' label is changed to 'Team Odds'
        EXPECTED: ![](index.php?/attachments/get/114764009)
        """
        pass

    def test_003_click_on_plus__functional_buttons_at_the_right_upper_corner_of_the_overlay(self):
        """
        DESCRIPTION: Click on '+/-' functional buttons at the right upper corner of the overlay
        EXPECTED: - Request 'price' is triggered to Banach
        EXPECTED: - Odds change accordingly and are displayed on the button
        EXPECTED: - 'Add Player' button is active
        """
        pass

    def test_004_press_add_player_button(self):
        """
        DESCRIPTION: Press 'Add Player' button
        EXPECTED: - User is redirected to pitch view
        EXPECTED: - Player is added and displayed on the corresponding position on pitch view
        """
        pass

    def test_005_return_to_player_card_view_and_press_plus_functional_button_till_user_reaches_max_value_limit(self):
        """
        DESCRIPTION: Return to player card view and press '+' functional button till user reaches max value limit
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - Odds are recalculated and displayed (spinner is displayed when user clicks several times the functional +/- buttons)
        """
        pass

    def test_006_press___functional_button_till_user_reaches_min_value_limit(self):
        """
        DESCRIPTION: Press '-' functional button till user reaches min value limit
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - Odds are recalculated and displayed
        """
        pass
