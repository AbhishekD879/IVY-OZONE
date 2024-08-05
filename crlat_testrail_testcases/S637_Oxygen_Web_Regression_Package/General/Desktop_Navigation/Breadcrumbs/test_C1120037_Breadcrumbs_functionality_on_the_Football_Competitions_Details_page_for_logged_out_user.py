import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C1120037_Breadcrumbs_functionality_on_the_Football_Competitions_Details_page_for_logged_out_user(Common):
    """
    TR_ID: C1120037
    NAME: Breadcrumbs functionality on the Football Competitions Details page for logged out user
    DESCRIPTION: This test case verifies Breadcrumbs functionality on the Football Competitions Details page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: 3. Navigate to Football Landing page
    PRECONDITIONS: 4. Click on 'Competitions' tab
    PRECONDITIONS: 5. Expand any Classes accordion and select any Type (Competition)
    PRECONDITIONS: 6. MAke sure that Matches' switcher is selected by default
    """
    keep_browser_open = True

    def test_001_verify_breadcrumbs_displaying_on_the_competitions_details_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying on the Competitions Details page
        EXPECTED: * Breadcrumbs are located below the 'Competitions' header
        EXPECTED: * Breadcrumbs are displayed in the next format: 'Home' > 'Football' > 'Competitions' > 'Type (Competition) name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_002_hover_the_mouse_over_breadcrumbs_trail(self):
        """
        DESCRIPTION: Hover the mouse over Breadcrumbs trail
        EXPECTED: * Breadcrumbs items are underlined as a link and clickable
        EXPECTED: * The last item in Breadcrumbs trail is NOT underlined and NOT clickable
        """
        pass

    def test_003_click_on_competitions_hyperlink_from_the_breadcrumbs_trail(self):
        """
        DESCRIPTION: Click on 'Competitions' hyperlink from the breadcrumbs trail
        EXPECTED: * Competitions Landing page is opened
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Sports Landing page: 'Home' > 'Football' > 'Competitions'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_004_navigate_to_competitions_details_page_and_click_on_sports_name_hyperlink_from_the_breadcrumbs_trail(self):
        """
        DESCRIPTION: Navigate to Competitions Details page and click on 'Sports Name' hyperlink from the Breadcrumbs trail
        EXPECTED: * Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the following format at the Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_005_navigate_to_competitions_details_page_and_click_on_back_button_on_the_competitions_header(self):
        """
        DESCRIPTION: Navigate to Competitions Details page and click on 'Back' button on the 'Competitions' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_006_navigate_to_competitions_details_page_and_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Navigate to Competitions Details page and click on 'Home' hyperlink from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass

    def test_007_navigate_to_competitions_details_page_and_chose_another_type_competition_from_change_competition_selector(self):
        """
        DESCRIPTION: Navigate to Competitions Details page and chose another Type (Competition) from 'Change Competition' selector
        EXPECTED: * Competitions Details page for chosen Type (Competition) is opened
        EXPECTED: * Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_008_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps 1-7
        EXPECTED: 
        """
        pass
