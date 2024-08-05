import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C2552889_Verify_displaying_of_Quick_Links_on_any_Sports_Landing_page(Common):
    """
    TR_ID: C2552889
    NAME: Verify displaying of Quick Links on any Sports Landing page
    DESCRIPTION: This test case verifies displaying of Quick Links on All Sports landing pages
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name> -> Quick Links  and configure 1 active Quick link for <Sport name> landing page
    PRECONDITIONS: 2. Load oxygen application and navigate to <Sport name> landing page
    PRECONDITIONS: [Tab name]- This tab is selected by default after accessing Sport Landing Page. Name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
    PRECONDITIONS: Ladbrokes Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    PRECONDITIONS: Coral design (now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    PRECONDITIONS: Note:
    PRECONDITIONS: Max amount of Quick Links, which can be displayed, is configurable in the CMS (CMS > System configuration > Structure > Sport Quick Links > maxAmount)
    """
    keep_browser_open = True

    def test_001_navigate_to_sport_name_landing_page_and_verify_that_configured_quick_link_is_displayed(self):
        """
        DESCRIPTION: Navigate to <Sport name> landing page and verify that configured Quick link is displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_002_click_anywhere_on_the_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_003_go_to_cms___sport_pages_sport_name___quick_links_and_configure_2nd_quick_link_for_the_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 2nd Quick link for the <Sport name> landing page
        EXPECTED: 
        """
        pass

    def test_004_go_to_oxygen_application_football_page_and_verify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Football page and verify that 2 configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_005_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_006_go_to_cms___sport_pages_sport_name___quick_links_and_configure_3rd_quick_link_for_sport_name_landing_page_with_a_long_namelong_enough_in_order_not_to_fit_the_remaining_width_of_the_screen(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 3rd Quick link for <Sport name> landing page with a long name(Long enough in order not to fit the remaining width of the screen)
        EXPECTED: 
        """
        pass

    def test_007_go_to_oxygen_application_football_page_and_verify_that_3_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Football page and verify that 3 configured Quick links are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_008_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated  to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application.
        """
        pass

    def test_009_go_to_cms_system_configuration__structure__sport_quick_links_module_set_max_number_of_quick_links_to_be_displayed_to_6(self):
        """
        DESCRIPTION: Go to CMS->System Configuration-> Structure-> Sport Quick Links module set max number of quick links to be displayed to 6.
        EXPECTED: 
        """
        pass

    def test_010_go_to_cms___sport_pages_sport_name___quick_links_and_configure_3_more_quick_links_in_order_to_have_6_active_quick_links_for_current_time_period(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name> -> Quick Links and configure 3 more Quick links in order to have 6 active Quick links for current Time period.
        EXPECTED: 
        """
        pass

    def test_011_go_to_oxygen_application_sport_name_landing_page_and_verify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application <Sport name> landing page and verify that 6 configured Quick links are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured Quick links are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_012_click_anywhere_on_one_of_the_newly_configured_quick_linksverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured quick links.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass
