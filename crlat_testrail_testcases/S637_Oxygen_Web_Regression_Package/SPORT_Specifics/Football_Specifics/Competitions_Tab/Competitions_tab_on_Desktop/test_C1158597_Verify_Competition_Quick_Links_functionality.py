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
class Test_C1158597_Verify_Competition_Quick_Links_functionality(Common):
    """
    TR_ID: C1158597
    NAME: Verify Competition Quick Links functionality
    DESCRIPTION: This test case verifies Competition Quick Links functionality
    PRECONDITIONS: *Note:*
    PRECONDITIONS: Be aware that names of competitions (Premier League, Championship, La Liga, Bundesliga, League One) are hardcoded and shouldn't be changed in OpenBet System for correct work on front-end.
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

    def test_004_hover_the_mouse_over_the_competition_quick_link(self):
        """
        DESCRIPTION: Hover the mouse over the Competition Quick Link
        EXPECTED: * The background of the whole section is changing
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_005_click_on_any_competition_quick_link(self):
        """
        DESCRIPTION: Click on any Competition Quick Link
        EXPECTED: * User is redirected to particular Competitions Details page
        EXPECTED: * Respective data is displayed on the page
        """
        pass

    def test_006_click_on_the_back_button_on_competitions_header(self):
        """
        DESCRIPTION: Click on the 'Back' button on Competitions header
        EXPECTED: * User is redirected to Competitions Landing page
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        """
        pass
