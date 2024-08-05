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
class Test_C65949627_Verify_display_of_Football_competitions(Common):
    """
    TR_ID: C65949627
    NAME: Verify  display of Football competitions
    DESCRIPTION: This Test case verifies  display of Football competitions
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    """
    keep_browser_open = True

    def test_001_verify_layout_of_competitions_tab(self):
        """
        DESCRIPTION: Verify layout of 'Competitions' tab
        EXPECTED: Desktop:
        EXPECTED: 'Popular' and 'A-Z' switchers should be displayed below Sports Sub Tabs
        EXPECTED: 'Popular' switcher should be selected by default and highlighted
        EXPECTED: Mobile:
        EXPECTED: Country Competitions should be displayed
        EXPECTED: 'A-Z' Competitions  should be displayed
        EXPECTED: All accordions are collapsed by default
        EXPECTED: 'A-Z'Competitions are ordered alphabetically
        """
        pass

    def test_002_verify_listing_of__available_competitions(self):
        """
        DESCRIPTION: Verify listing of  available competitions
        EXPECTED: For mobile/Tablet:
        EXPECTED: The leagues (types) are displayed in the list view
        EXPECTED: For Desktop:
        EXPECTED: The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_003_verify_quick_links(self):
        """
        DESCRIPTION: Verify Quick links
        EXPECTED: For Desktop and mobile:
        EXPECTED: Quick link with Svg icon should be displayed and navigated according to  cms configurations
        """
        pass
