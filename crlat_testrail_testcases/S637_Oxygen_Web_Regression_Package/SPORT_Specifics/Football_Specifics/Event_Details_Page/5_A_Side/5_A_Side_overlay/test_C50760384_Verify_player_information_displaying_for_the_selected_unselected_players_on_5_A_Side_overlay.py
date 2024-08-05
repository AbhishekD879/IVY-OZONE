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
class Test_C50760384_Verify_player_information_displaying_for_the_selected_unselected_players_on_5_A_Side_overlay(Common):
    """
    TR_ID: C50760384
    NAME: Verify player information displaying for the  selected/unselected players on  '5-A-Side' overlay
    DESCRIPTION: This test case verifies player information displaying for the  selected/unselected players on '5-A-Side' overlay
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap 'Build A Team' button
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True

    def test_001_verify_player_information_displaying_for_no_selected_players(self):
        """
        DESCRIPTION: Verify player information displaying for NO selected Players
        EXPECTED: The following player information is displayed for NO selected Players:
        EXPECTED: * Positions (corresponding to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        """
        pass

    def test_002_clicktap_plus_add_button__select_any_player__choose_some_stats_value_for_the_player_eg_2_for_shots_on_target__clicktap_add_playerverify_player_information_displaying_for_the_selected_players(self):
        """
        DESCRIPTION: Click/Tap '+' (add) button > Select any player > Choose some stats value for the player (e.g. '2' for 'Shots On Target') > Click/Tap 'Add player'.
        DESCRIPTION: Verify player information displaying for the selected Players.
        EXPECTED: The following player information is displayed for the selected Players:
        EXPECTED: * Positions (corresponding to selected player name e.g. B.Valero)
        EXPECTED: * Statistics (corresponding to selected stat and value e.g. 2+ Shots On Target)
        """
        pass
