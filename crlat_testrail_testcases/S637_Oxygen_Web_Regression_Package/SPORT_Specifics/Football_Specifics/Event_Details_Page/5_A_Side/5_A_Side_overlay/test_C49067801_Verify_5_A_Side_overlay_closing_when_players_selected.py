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
class Test_C49067801_Verify_5_A_Side_overlay_closing_when_players_selected(Common):
    """
    TR_ID: C49067801
    NAME: Verify '5-A-Side' overlay closing when players selected
    DESCRIPTION: This test case verifies '5-A-Side' overlay closing when players are selected
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

    def test_001_clicktap_plus_add_button__select_any_player__click_add_player(self):
        """
        DESCRIPTION: Click/Tap '+' (add) button > Select any player > Click 'Add player'
        EXPECTED: * 'Pitch View' section is displayed with the selected player
        """
        pass

    def test_002_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: Pop-up is displayed with the following content:
        EXPECTED: * '5-A-Side' title
        EXPECTED: * 'If you leave now, your team will not be saved' text
        EXPECTED: * 'Leave' button and 'Stay' button
        """
        pass

    def test_003_clicktap_on_stay_button(self):
        """
        DESCRIPTION: Click/Tap on 'Stay' button
        EXPECTED: * Pop-up is closed
        EXPECTED: * 'Pitch View' section is displayed with the selected player
        """
        pass

    def test_004_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: Pop-up is displayed with the same content
        """
        pass

    def test_005_clicktap_on_leave_button(self):
        """
        DESCRIPTION: Click/Tap on 'Leave' button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        pass

    def test_006_clicktap_build_a_team_buttonverify_if_the_previous_state_is_not_saved(self):
        """
        DESCRIPTION: Click/Tap 'Build A Team' button.
        DESCRIPTION: Verify if the previous state is not saved.
        EXPECTED: * '5-A-Side' overlay is opened
        EXPECTED: * There are no added players on the 'Pitch View' section
        """
        pass
