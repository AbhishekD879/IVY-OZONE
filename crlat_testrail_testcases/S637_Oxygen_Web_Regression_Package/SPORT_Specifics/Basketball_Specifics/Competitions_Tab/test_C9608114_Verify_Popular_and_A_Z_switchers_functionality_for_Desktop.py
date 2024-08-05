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
class Test_C9608114_Verify_Popular_and_A_Z_switchers_functionality_for_Desktop(Common):
    """
    TR_ID: C9608114
    NAME: Verify 'Popular' and 'A-Z' switchers functionality for Desktop
    DESCRIPTION: This test case verifies 'Popular' and 'A-Z' switchers functionality for Desktop
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The sub-categories (Classes) are CMS configurable on Competitions page and are ordered according to settings in the CMS.
    PRECONDITIONS: 2. Types (Competitions) are ordered by OpenBet display order (lowest display order at the top)
    PRECONDITIONS: For setting sub-categories in CMS navigate to 'System-configuration' -> 'Competitions' and put class ID's in 'InitialClassIDs' or 'A-ZClassIDs' field.
    PRECONDITIONS: **(!)** 'CompetitionsFootball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
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
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        """
        pass

    def test_004_verify_navigation_between_popular_and_a_z_switchers(self):
        """
        DESCRIPTION: Verify navigation between 'Popular' and 'A-Z' switchers
        EXPECTED: * The User must be able to select 'Popular' and 'A-Z' switchers
        EXPECTED: * Selected switcher is highlighted by red line
        EXPECTED: * If user selects 'Popular'/'A-Z' switcher they will be redirected to 'Popular'/'A-Z' page
        """
        pass

    def test_005_verify_content_of_page_when_popular_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Popular' switcher is selected
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * All Classes accordion are collapsible/expandable
        EXPECTED: * The sub-categories (Classes) accordions are ordered according to settings in the CMS
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        EXPECTED: * The leagues (Types) are ordered by OpenBet display order
        """
        pass

    def test_006_verify_content_of_page_when_a_z_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'A-Z' switcher is selected
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * All Classes accordion are collapsible/expandable
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        EXPECTED: * The sub-categories (Classes) accordion are displayed in Alphabetical order
        EXPECTED: * The leagues (Types) are ordered by OpenBet display order
        """
        pass

    def test_007_verify_content_of_page_when_populara_z_switcher_is_selected_and_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of page when 'Popular'/'A-Z' switcher is selected and there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on 'Popular'/'A-Z' pages
        """
        pass
