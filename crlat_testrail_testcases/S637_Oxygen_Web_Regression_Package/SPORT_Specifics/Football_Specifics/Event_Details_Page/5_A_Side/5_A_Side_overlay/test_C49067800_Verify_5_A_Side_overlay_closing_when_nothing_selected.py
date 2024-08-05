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
class Test_C49067800_Verify_5_A_Side_overlay_closing_when_nothing_selected(Common):
    """
    TR_ID: C49067800
    NAME: Verify '5-A-Side' overlay closing when nothing selected
    DESCRIPTION: This test case verifies '5-A-Side' overlay closing when no players are selected
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

    def test_001_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        pass

    def test_002_clicktap_build_team_button(self):
        """
        DESCRIPTION: Click/Tap 'Build team' button
        EXPECTED: * '5-A-Side' overlay is opened
        EXPECTED: * First formation is selected
        """
        pass

    def test_003_clicktap_plus_add_button__select_any_player__clicktap_add_player(self):
        """
        DESCRIPTION: Click/Tap '+' (add) button > Select any player > Click/Tap 'Add player'
        EXPECTED: * 'Pitch View' section is displayed with the selected player
        """
        pass

    def test_004_clicktap_on_formation_2_and_back_on_formation_1(self):
        """
        DESCRIPTION: Click/Tap on formation #2 and back on formation #1
        EXPECTED: * 'Pitch View' section is displayed with NO players selected
        """
        pass

    def test_005_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        pass
