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
class Test_C60079290_Verify_Matches_and_Outrights_switchers_functionality_on_Basketball_Competition_Details_page_for_Desktop(Common):
    """
    TR_ID: C60079290
    NAME: Verify 'Matches' and 'Outrights' switchers functionality on Basketball Competition Details page for Desktop
    DESCRIPTION: This test case verifies 'Matches' and 'Outrights' switchers functionality on Basketball Competition Details page for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion
    PRECONDITIONS: Note! To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Basketball**. Events for those classes should be present as well.
    """
    keep_browser_open = True

    def test_001_select_any_competition_type_within_expanded_class(self):
        """
        DESCRIPTION: Select any competition (type) within expanded class
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed below Competitions header and Breadcrumbs trail
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_002_verify_navigation_between_matches_and_outrights_switchers(self):
        """
        DESCRIPTION: Verify navigation between 'Matches' and 'Outrights' switchers
        EXPECTED: * The User must be able to select 'Matches' and 'Outrights' switchers
        EXPECTED: * Selected switcher is highlighted by red line
        EXPECTED: * If user selects 'Matches'/'Outrights' switcher they will be redirected to 'Matches'/'Outrights' page
        """
        pass

    def test_003_verify_content_of_page_when_matches_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Matches' switcher is selected
        EXPECTED: * List of events grouped by days is displayed
        EXPECTED: * Events are ordered by start time
        """
        pass

    def test_004_verify_content_of_page_when_outrights_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Outrights' switcher is selected
        EXPECTED: * The Events accordions are loaded on the page
        EXPECTED: * The first Events accordion is expanded by default the rest are collapsed
        EXPECTED: * The Markets sub-accordions are displayed within expanded Event accordion
        EXPECTED: * The first Markets sub-accordion is expanded by default the rest are collapsed
        EXPECTED: * The selections are displayed in Horizontal position within expanded Markets sub-accordion
        """
        pass

    def test_005_verify_content_of_page_when_matchesoutrights_switcher_is_selected_and_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of page when 'Matches'/'Outrights' switcher is selected and there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on 'Matches'/'Outrights' pages
        """
        pass
