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
class Test_C49405229_Verify_reselecting_player_on_Pitch_View_section_5_A_Side_tab(Common):
    """
    TR_ID: C49405229
    NAME: Verify reselecting player on 'Pitch View' section ( '5-A-Side' tab)
    DESCRIPTION: This test case verifies the ability to reselect previously chosen players on 'Pitch View' section on '5-A-Side' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click/Tap '+' (add) button > Select any player > Click/Tap 'Add player'
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

    def test_001_verify_selected_players_on_pitch_view_section(self):
        """
        DESCRIPTION: Verify selected player(s) on 'Pitch View' section
        EXPECTED: 'Pitch View' section is displayed with the selected player(s)
        """
        pass

    def test_002_clicktap_on_any_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on any previously selected player
        EXPECTED: 'Player Card' view of previously selected player is displayed with appropriate statistics info for that player (if available):
        EXPECTED: ![](index.php?/attachments/get/113306236)
        """
        pass

    def test_003_clicktap_on_back_button_on_player_card_view(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button on 'Player Card' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player and odds remain unchanged
        """
        pass

    def test_004_clicktap_on_plus_add_button_for_any_position(self):
        """
        DESCRIPTION: Click/Tap on '+' (add) button for any position
        EXPECTED: 'Player List' view is displayed
        """
        pass

    def test_005_select_any_player_from_the_list(self):
        """
        DESCRIPTION: Select any player from the list
        EXPECTED: 'Player Card' view is displayed
        """
        pass

    def test_006__clicktap_on_back_button_on_player_card_view_clicktap_on_back_button_on_player_list_view(self):
        """
        DESCRIPTION: * Click/Tap on 'Back' button on 'Player Card' view
        DESCRIPTION: * Click/Tap on 'Back' button on 'Player List' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player is not added to the position; '+' button to add a player is displayed
        EXPECTED: * Odds remain unchanged
        """
        pass
