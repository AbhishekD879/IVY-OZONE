import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C62167379_Navigate_Cricket_100(Common):
    """
    TR_ID: C62167379
    NAME: Navigate Cricket 100
    DESCRIPTION: This test case verifies navigation through Cricket 100 pages is correct:
    DESCRIPTION: Matches
    DESCRIPTION: Inplay
    DESCRIPTION: Competitions
    PRECONDITIONS: Load the application.
    PRECONDITIONS: Go to Sports-Cricket
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: 1.User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be displayed by default for the League.
        EXPECTED: 2.Inplay page should be loaded
        EXPECTED: -All events which are available are displayed for the League.
        """
        pass

    def test_002_clicktap_on_inplay_tab(self):
        """
        DESCRIPTION: Click/Tap on Inplay tab.
        EXPECTED: Inplay page should be loaded.
        EXPECTED: -All events which are available are displayed for the League.
        """
        pass

    def test_003_clicktap_on_competitions_tab(self):
        """
        DESCRIPTION: Click/Tap on Competitions Tab.
        EXPECTED: All events which are available are displayed for the League.
        """
        pass
