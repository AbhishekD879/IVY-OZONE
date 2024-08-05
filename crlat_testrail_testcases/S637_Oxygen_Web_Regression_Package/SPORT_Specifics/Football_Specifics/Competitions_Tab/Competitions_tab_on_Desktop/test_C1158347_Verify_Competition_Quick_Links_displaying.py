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
class Test_C1158347_Verify_Competition_Quick_Links_displaying(Common):
    """
    TR_ID: C1158347
    NAME: Verify Competition Quick Links displaying
    DESCRIPTION: This test case verifies Competition Quick Links displaying
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is loaded
        """
        pass

    def test_003_click_on_competitions_tab(self):
        """
        DESCRIPTION: Click on 'Competitions' tab
        EXPECTED: Competitions page is opened with the following elements:
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * Competitions are displayed in accordions
        """
        pass

    def test_004_verify_competition_quick_links_displaying(self):
        """
        DESCRIPTION: Verify Competition Quick Links displaying
        EXPECTED: * 5 Competition Quick Links are displayed for &gt;=1280px width in the next order:
        EXPECTED: * Premier League
        EXPECTED: * Championship
        EXPECTED: * La Liga
        EXPECTED: * Bundesliga
        EXPECTED: * League One
        EXPECTED: * 3 Competition Quick Links are displayed for &lt;1280px width in the next order:
        EXPECTED: * Premier League
        EXPECTED: * Championship
        EXPECTED: * La Liga
        EXPECTED: * The size of Competition Quick Links sections is changed according to screen width
        """
        pass

    def test_005_verify_competition_quick_links_content(self):
        """
        DESCRIPTION: Verify Competition Quick Links content
        EXPECTED: Competition Quick Links section consists of:
        EXPECTED: * Country flag at the top left corner of section
        EXPECTED: * Country name next to Flag
        EXPECTED: * 'BYB' icon (if available) next to Country name **was removed in scope of BMA-43761**
        EXPECTED: * Competition name
        EXPECTED: * Arrow at the right side of the section
        """
        pass
