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
class Test_C1053929_Verify_Matches_and_Outrights_switchers_functionality_on_Competitions_page_for_Desktop(Common):
    """
    TR_ID: C1053929
    NAME: Verify 'Matches' and 'Outrights' switchers functionality on Competitions page for Desktop
    DESCRIPTION: This test case verifies 'Matches' and 'Outrights' switchers functionality on Competitions page for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The sub-categories (Classes) are CMS configurable on Competitions page and are ordered according to settings in the CMS.
    PRECONDITIONS: 2. Types (Competitions) are ordered by OpenBet display order (lowest display order at the top)
    PRECONDITIONS: For setting sub-categories in CMS navigate to 'System-configuration' -> 'Competitions' and put class ID's in 'InitialClassIDs' or 'A-ZClassIDs' field.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page__gt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        pass

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed below Competitions header and Breadcrumbs trail in the same row as 'Market Selector'
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_004_verify_navigation_between_matches_and_outrights_switchers(self):
        """
        DESCRIPTION: Verify navigation between 'Matches' and 'Outrights' switchers
        EXPECTED: * The User must be able to select 'Matches' and 'Outrights' switchers
        EXPECTED: * Selected switcher is highlighted by red line
        EXPECTED: * If user selects 'Matches'/'Outrights' switcher they will be redirected to 'Matches'/'Outrights' page
        """
        pass

    def test_005_verify_content_of_page_when_matches_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Matches' switcher is selected
        EXPECTED: * List of events grouped by days is displayed
        EXPECTED: * Events are ordered by start time
        """
        pass

    def test_006_verify_content_of_page_when_outrights_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Outrights' switcher is selected
        EXPECTED: * The Events accordions are loaded on the page
        EXPECTED: * The first Events accordion is expanded by default the rest are collapsed
        EXPECTED: * The Markets sub-accordions are displayed within expanded Event accordion
        EXPECTED: * The first Markets sub-accordion is expanded by default the rest are collapsed
        EXPECTED: * The selections are displayed in Horizontal position within expanded Markets sub-accordion
        """
        pass

    def test_007_verify_content_of_page_when_matchesoutrights_switcher_is_selected_and_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of page when 'Matches'/'Outrights' switcher is selected and there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on 'Matches'/'Outrights' pages
        """
        pass
