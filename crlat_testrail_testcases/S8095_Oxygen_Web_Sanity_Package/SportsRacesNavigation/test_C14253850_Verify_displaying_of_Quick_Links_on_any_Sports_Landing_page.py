import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C14253850_Verify_displaying_of_Quick_Links_on_any_Sports_Landing_page(Common):
    """
    TR_ID: C14253850
    NAME: Verify displaying of 'Quick Links' on any Sports Landing page
    DESCRIPTION: This test case verifies displaying of Quick Links on All Sports landing pages
    DESCRIPTION: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    DESCRIPTION: AUTOTEST [C58068809]
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name> -> Quick Links  and configure 1 active Quick link for <Sport name> landing page
    PRECONDITIONS: 2. Set 'Active'/'Inactive' flag to 'Active' for the configured 'Quick link' for the <Sport name> landing page to make it visible on the front end
    PRECONDITIONS: 3. Load the application
    PRECONDITIONS: 4. Navigate to <Sport name> landing page
    PRECONDITIONS: [Tab name] - This tab is selected by default after accessing the Sport Landing Page. The name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in the application
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Max amount of Quick Links, which can be displayed, is configurable in the CMS (CMS > System configuration > Structure > Sport Quick Links > maxAmount)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_configured_quick_link_is_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Verify displaying of configured 'Quick link' is displayed on <Sport name> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick link' is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * 'Quick link' is stretched to fit the width of the screen.
        """
        pass

    def test_002_click_anywhere_on_the_configured_quick_linkverify_redirection_to_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the configured quick link.
        DESCRIPTION: Verify redirection to specific page (URL) configured in CMS.
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_003_go_to_cms___sports_pages___sport_name___quick_links_configure_2nd_quick_link_for_sport_name_landing_page_with_a_long_namelong_enough_in_order_not_to_fit_the_remaining_width_of_the_screen(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links. Configure 2nd Quick link for <Sport name> landing page with a long name(Long enough in order not to fit the remaining width of the screen).
        EXPECTED: 
        """
        pass

    def test_004_go_to_the_application_sport_name_landing_pageverify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application <Sport name> landing page.
        DESCRIPTION: Verify that 2 configured 'Quick links' are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**::
        EXPECTED: * 'Quick links' are displayed in one row as 2 separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as raws in the list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        pass

    def test_005_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated  to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application.
        """
        pass

    def test_006_go_to_cms___system_configuration___structure___sport_quick_links_moduleset_the_maxamount_number_of_quick_links_to_be_displayed(self):
        """
        DESCRIPTION: Go to CMS -> System Configuration -> Structure -> Sport Quick Links module.
        DESCRIPTION: Set the 'maxAmount' number of 'Quick links' to be displayed.
        EXPECTED: 
        """
        pass

    def test_007_go_to_cms___sports_pages___sport_name___quick_links_configure_more_quick_links_in_order_to_have_maxamount_active_quick_links_for_the_current_time_period(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links. Configure more 'Quick links' in order to have 'maxAmount' active 'Quick links' for the current Time period.
        EXPECTED: 
        """
        pass

    def test_008_go_to_the_application_sport_name_landing_pageverify_that_maxamount_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application <Sport name> landing page.
        DESCRIPTION: Verify that 'maxAmount' configured 'Quick links' are displayed.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * 'Quick links' container is displayed on [Tab name] of <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are displayed on [Tab name] of <Sport name> landing page
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed as 'maxAmount' separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as rows in the list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        pass

    def test_009_click_anywhere_on_one_of_the_newly_configured_quick_linksverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured 'Quick links'.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_010_select_any_other_tab_on_the_sport_name_landing_page_eg_outrights_coupons_etcverify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the <Sport name> landing page (e.g. Outrights, Coupons, etc.)
        DESCRIPTION: Verify displaying of 'Quick links' on other tabs.
        EXPECTED: * Configured 'Quick links' are displayed only on the <Sport name> landing page -> 'Matches' tab
        EXPECTED: * 'Quick links' container is NOT displayed on other tabs on <Sport name> landing page
        EXPECTED: * Configured 'Quick links' are NOT displayed on other tabs on <Sport name> landing page
        """
        pass

    def test_011_go_to_the_homepage___featured_tab_and_observe_the_quick_links_sectionverify_displaying_of_sport_name_landing_page_configured_quick_links_on_the_homepage(self):
        """
        DESCRIPTION: Go to the Homepage -> 'Featured' tab and observe the 'Quick links' section.
        DESCRIPTION: Verify displaying of <Sport name> landing page configured 'Quick links' on the Homepage.
        EXPECTED: * Configured 'Quick link' for <Sport name> landing page is NOT displayed on the Homepage
        EXPECTED: * Only 'Quick links' that are configured for the Homepage are shown (if there are some)
        EXPECTED: 'Quick links' container and links are NOT displayed If no 'Quick links' are configured for the Homepages.
        """
        pass

    def test_012_go_to_cms___sports_pages___sport_name___quick_links_set_activeinactive_flag_for_the_configured_quick_link_for_sport_name_landing_page_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> <Sport name> -> Quick Links. Set "Active"/"Inactive" flag for the configured 'Quick link' for <Sport name> landing page to 'Inactive'.
        EXPECTED: 
        """
        pass

    def test_013_go_to_the_appnavigate_to_the_sport_name_landing_pageverify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to the app.
        DESCRIPTION: Navigate to the <Sport name> landing page.
        DESCRIPTION: Verify that 'Quick link' is no longer displayed.
        EXPECTED: * 'Quick links' container is NOT displayed.
        EXPECTED: * 'Quick link' is no longer displayed.
        """
        pass
