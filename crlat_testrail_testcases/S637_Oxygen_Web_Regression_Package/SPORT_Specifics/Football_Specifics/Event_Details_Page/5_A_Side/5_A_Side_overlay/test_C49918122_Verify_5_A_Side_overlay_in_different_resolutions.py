import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C49918122_Verify_5_A_Side_overlay_in_different_resolutions(Common):
    """
    TR_ID: C49918122
    NAME: Verify '5-A-Side' overlay in different resolutions
    DESCRIPTION: This test case verifies '5-A-Side' overlay displaying in different screen resolutions on tablet and desktop
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build A Team' button
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_load_the_app_with_preconditions_on_tabletdesktop_with_screen_resolution_from_320px_till_969px(self):
        """
        DESCRIPTION: Load the app with preconditions on tablet/desktop with screen resolution from 320px till 969px
        EXPECTED: * '5-A-Side' overlay sticks to the bottom
        EXPECTED: * It's max width is 480px
        EXPECTED: ![](index.php?/attachments/get/65355401)
        """
        pass

    def test_002_load_the_app_with_preconditions_on_tabletdesktop_with_screen_resolution_970px_and_higher(self):
        """
        DESCRIPTION: Load the app with preconditions on tablet/desktop with screen resolution 970px and higher
        EXPECTED: * '5-A-Side' overlay is centered
        EXPECTED: * It's max width is 740px
        EXPECTED: ![](index.php?/attachments/get/65355402)
        """
        pass
