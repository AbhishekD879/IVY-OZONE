import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65949628_Verify_Football_competitions_navigations(Common):
    """
    TR_ID: C65949628
    NAME: Verify Football competitions navigations
    DESCRIPTION: This Test case verifies  Football competitions navigations
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    """
    keep_browser_open = True

    def test_001_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: For Desktop:
        EXPECTED: There are 'Matches and 'Outrights' tabs
        EXPECTED: 'Matches' tab is selected by default
        EXPECTED: 'Results' and 'League Table' widgets are displayed if available
        EXPECTED: For mobile/Tablet:
        EXPECTED: Events from the relevant league (type) are displayed
        EXPECTED: There are 3 tabs (navigation buttons) on the page: 'Matches', 'Results', 'Outrights', standings
        EXPECTED: 'Matches' tab is selected by default
        """
        pass

    def test_002_verify_market_switcher_on_matches_tab(self):
        """
        DESCRIPTION: Verify market switcher on matches tab
        EXPECTED: Desktop:
        EXPECTED: Match result market switcher should be selected as default
        EXPECTED: Market switcher dropdown should be displayed and when clicked on specfic market it should be displayed.
        EXPECTED: Mobile:
        EXPECTED: Match result market switcher should be selected as default
        EXPECTED: Market switcher dropdown should be displayed and when clicked on specfic market it should be displayed.
        """
        pass

    def test_003_verify_change_competition_dropdown(self):
        """
        DESCRIPTION: Verify change competition dropdown
        EXPECTED: Desktop and mobile:
        EXPECTED: change competition dropdown should be displayed and when selected on specfic competition it should be displayed.
        """
        pass

    def test_004_verify_signpostings_and_favpurite_icons(self):
        """
        DESCRIPTION: Verify Signpostings and Favpurite icons
        EXPECTED: * Sign postings (build your bet, price boost etc)
        EXPECTED: Favourite (star) icon should be displayed
        """
        pass
