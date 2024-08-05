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
class Test_C892355_Breadcrumbs_functionality_on_the_Olympic_Sports_pages(Common):
    """
    TR_ID: C892355
    NAME: Breadcrumbs functionality on the Olympic Sports pages
    DESCRIPTION: This test case verifies Breadcrumbs functionality on the Olympic Sports pages.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Olympics Landing page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Labels for "Matches" tab for every Olympics Sport are CMS configurable and could be different from 'Matches' depends on settings.
    """
    keep_browser_open = True

    def test_001_verify_breadcrumbs_displaying_at_the_olympics_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Olympics Landing page
        EXPECTED: * Breadcrumbs are located below the 'Olympics' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Olympics Landing page: 'Home' > 'Olympics'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_002_choose_any_sport_from_sports_list_at_the_olympics_landing_page(self):
        """
        DESCRIPTION: Choose any Sport from Sports list at the Olympics Landing page
        EXPECTED: Sports Olympics Landing page is opened
        """
        pass

    def test_003_verify_breadcrumbs_displaying_at_the_sports_olympics_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Sports Olympics Landing page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Olympics Landing page: 'Home' > 'Olympics' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_004_choose_outrights_tab_from_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Choose 'Outrights' tab from Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab (e.g. 'Outrights')
        """
        pass

    def test_005_repeat_step_4_for_all_tabs_in_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Repeat step 4 for all tabs in Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab
        """
        pass

    def test_006_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Olympics Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Sports Olympics Landing page: 'Home' > 'Olympics' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Sports Olympics Landing page or as mentioned in Preconditions)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_007_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_008_click_on_olympics_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Olympics' hyperlink from the breadcrumbs
        EXPECTED: * Olympics Landing page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_009_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass
