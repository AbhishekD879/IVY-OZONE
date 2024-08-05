import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C47660680_Verify_5_A_Side_Launcher_and_URL_structure(Common):
    """
    TR_ID: C47660680
    NAME: Verify 5-A-Side Launcher and URL structure
    DESCRIPTION: This test case verifies pitch overlay launching and URL structure.
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the '5-A-Side' tab should be switched off in case Static Block is disabled because it's part of the path for reaching the '5-A-Side' overlay.
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Select the '5-A-Side' tab
    """
    keep_browser_open = True

    def test_001_verify_url_structure_when_5_a_side_tab_is_selected(self):
        """
        DESCRIPTION: Verify URL Structure when '5-A-Side' tab is selected
        EXPECTED: URL ends with event_id/5-a-side
        """
        pass

    def test_002_clicktap_on_build_a_team_button_cms_configurable(self):
        """
        DESCRIPTION: Click/Tap on 'Build A Team' button (CMS configurable)
        EXPECTED: '5-A-Side' overlay is loaded
        """
        pass

    def test_003_verify_url_structure(self):
        """
        DESCRIPTION: Verify URL Structure
        EXPECTED: URL ends with event_id/5-a-side/pitch
        """
        pass

    def test_004__copy_url_open_a_new_browser_tab_and_paste_url(self):
        """
        DESCRIPTION: * Copy URL.
        DESCRIPTION: * Open a new browser tab and paste URL.
        EXPECTED: * Corresponding event details page is loaded
        EXPECTED: * '5-A-Side' overlay is launched
        """
        pass
