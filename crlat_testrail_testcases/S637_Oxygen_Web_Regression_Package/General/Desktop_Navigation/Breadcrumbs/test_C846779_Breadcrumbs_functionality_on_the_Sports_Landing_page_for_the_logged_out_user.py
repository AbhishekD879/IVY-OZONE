import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C846779_Breadcrumbs_functionality_on_the_Sports_Landing_page_for_the_logged_out_user(Common):
    """
    TR_ID: C846779
    NAME: Breadcrumbs functionality on the Sports Landing page for the logged out user
    DESCRIPTION: This test case verifies breadcrumbs functionality on the Sports Landing pages for the logged out user.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    DESCRIPTION: **Auto-test:** [C9689874](https://ladbrokescoral.testrail.com/index.php?/cases/view/9689874)
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged out
    PRECONDITIONS: 3. Sports Landing page is opened
    PRECONDITIONS: 4. 'Matches'->'Today' tab is opened by default
    """
    keep_browser_open = True

    def test_001_verify_breadcrumbs_displaying_at_the_sports_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Sports Landing page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Landing page:
        EXPECTED: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_002_choose_outrights_tab_from_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Choose 'Outrights' tab from Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab (e.g. 'Outrights')
        """
        pass

    def test_003_repeat_step_2_for_all_tabs_in_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Repeat step 2 for all tabs in Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab
        """
        pass

    def test_004_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Sports Landing page:
        EXPECTED: 'Home' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_005_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_006_click_on_home_hyperlink__from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink  from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass
