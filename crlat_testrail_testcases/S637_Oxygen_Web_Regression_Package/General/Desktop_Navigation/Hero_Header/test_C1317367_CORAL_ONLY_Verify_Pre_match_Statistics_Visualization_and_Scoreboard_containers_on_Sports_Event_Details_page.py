import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1317367_CORAL_ONLY_Verify_Pre_match_Statistics_Visualization_and_Scoreboard_containers_on_Sports_Event_Details_page(Common):
    """
    TR_ID: C1317367
    NAME: [CORAL ONLY] Verify Pre-match Statistics, Visualization and Scoreboard containers on Sports Event Details page
    DESCRIPTION: This test case verifies Pre-match Statistics, Visualization and Scoreboard containers on Sports Event Details page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Sports Event Details page is opened
    PRECONDITIONS: **Links to pre-match stats, scoreboards and visualization related info:**
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Football+Pre-match+Statistics
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Football+3D+Live+VIS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/VIS%3A+Tennis
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Migrated+Grand+Parade+Scoreboards
    """
    keep_browser_open = True

    def test_001_verify_pre_match_statistic_displaying_for_pre_match_events_football_only(self):
        """
        DESCRIPTION: Verify Pre-match Statistic displaying for pre-match events (Football only)
        EXPECTED: Container for pre-match statistic has the following sizes for all breakpoints:
        EXPECTED: * width: 500px
        EXPECTED: * height: 317px
        """
        pass

    def test_002_verify_visualization_displaying_for_live_events_football_and_tennis(self):
        """
        DESCRIPTION: Verify Visualization displaying for live events (Football and Tennis)
        EXPECTED: * Container for **Football/Tennis** Visualization has the following sizes for all breakpoints:
        EXPECTED: * width: 500px
        EXPECTED: * height: 280px
        """
        pass

    def test_003_verify_scoreboard_displaying_for_live_events_football_and_tennis(self):
        """
        DESCRIPTION: Verify Scoreboard displaying for live events (Football and Tennis)
        EXPECTED: * Container for **Football** Scoreboard has the following sizes for all breakpoints:
        EXPECTED: * width: 500px
        EXPECTED: * height: 280px
        EXPECTED: * Container for **Tennis** Scoreboard has the following sizes for different  breakpoints:
        EXPECTED: **1600px/1280px**
        EXPECTED: * width: 640px
        EXPECTED: * height depends on proportions
        EXPECTED: **1025px**
        EXPECTED: * width: 555px
        EXPECTED: * height depends on proportions
        EXPECTED: **970px**
        EXPECTED: * width: 500px
        EXPECTED: * height depends on proportions
        """
        pass

    def test_004_verify_scoreboard_displaying_for_live_events_basketball_cricket_rugby_and_darts(self):
        """
        DESCRIPTION: Verify Scoreboard displaying for live events (Basketball, Cricket, Rugby and Darts)
        EXPECTED: * Containers for **Basketball, Cricket, Rugby and Darts** Scoreboard are extended on the whole width of the main view
        EXPECTED: * Scoreboard is shown, if it is present in **scoreboard** response (in Network tab)
        """
        pass
