import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870195_GHNavigation_journeys(Common):
    """
    TR_ID: C44870195
    NAME: GHNavigation journeys
    DESCRIPTION: GH Navigation journeys:
    DESCRIPTION: Home page, Highlights tab -> Tap on ""View All Greyhounds Betting"" - will lead to landing page
    DESCRIPTION: Home page, carousel link or Tab bar - App Sports (Menu) -> Tap on Greyhounds will lead to landing page
    PRECONDITIONS: Load Site
    PRECONDITIONS: User is on Home Page
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds Landing page
        EXPECTED: User should land on Greyhounds Race Landing Page.
        EXPECTED: The page contains the following tabs :
        EXPECTED: NEXT RACES
        EXPECTED: TODAY
        EXPECTED: TOMORROW
        EXPECTED: BY meeting
        EXPECTED: By Time
        """
        pass

    def test_002_verify_next_races_tab(self):
        """
        DESCRIPTION: Verify 'NEXT RACES' tab
        EXPECTED: All the next races that are about to start should load in order of start time, earliest being on the top.
        EXPECTED: Each event displays the first 3 entries (count can be increased as configured in the CMS) with an option to view the full race card by clicking on 'MORE'
        EXPECTED: User should be able to scroll up and down the list of races.
        """
        pass
