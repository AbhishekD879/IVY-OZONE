import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726399_Event_Hub_Verify_displaying_of_Quick_Links_on_Event_hub(Common):
    """
    TR_ID: C9726399
    NAME: Event Hub: Verify displaying of Quick Links on Event hub
    DESCRIPTION: This test case verifies displaying of Quick Links on Event Hub
    PRECONDITIONS: 1. Go to CMS > Sport Pages > Event Hub and configure 1 active Quick link for Event Hub
    PRECONDITIONS: 2. Load oxygen application and navigate to Event hub tab
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_configured_quick_link_on_event_hub(self):
        """
        DESCRIPTION: Verify displaying of configured Quick link on Event Hub
        EXPECTED: * Quick links container is displayed on Event Hub.
        EXPECTED: * Configured Quick link is displayed on Event Hub.
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        pass

    def test_002_click_anywhere_on_the_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the configured quick link.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigate to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_003_go_to_cms__sport_pages__event_hub__and_configure_2nd_quick_link(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > Event Hub  and configure 2nd Quick link.
        EXPECTED: 
        """
        pass

    def test_004_go_to_oxygen_application_event_hub_and_verify_that_2_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Event Hub and verify that 2 configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed on Event Hub.
        EXPECTED: * Configured Quick links are displayed on Event hub.
        EXPECTED: **[CORAL]**:
        EXPECTED: * Quick links are displayed in the carousel as 2 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
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

    def test_006_go_to_cms___sport_pages__event_hub_and_configure_3rd_quick_link_for_event_hub_with_a_long_namelong_enough_in_order_not_to_fit_the_remaining_width_of_the_screen(self):
        """
        DESCRIPTION: Go to CMS  > Sport Pages > Event Hub and configure 3rd Quick link for Event Hub with a long name(Long enough in order not to fit the remaining width of the screen)
        EXPECTED: 
        """
        pass

    def test_007_go_to_oxygen_application_event_hub_and_verify_that_3_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Event Hub and verify that 3 configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed on Event Hub.
        EXPECTED: * Configured Quick links are displayed on Event Hub.
        EXPECTED: **[CORAL]**:
        EXPECTED: * Quick link are displayed displayed in the carousel as 3 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * 3d Quick link is cut off. Only part that can fit the remaining width of the screen is shown.
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
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

    def test_009_go_to_cms_system_configuration_structure__sport_quick_links_module_and_set_max_number_of_quick_links_to_be_displayed_in_one_time_period_to_6(self):
        """
        DESCRIPTION: Go to CMS->System Configuration->Structure-> Sport Quick Links module and set max number of quick links to be displayed in one Time period to 6.
        EXPECTED: 
        """
        pass

    def test_010_go_to_cms__sport_pages_event_hub_and_configure_3_more_quick_links_in_order_to_have_6_active_quick_links_for_current_time_period(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages >Event Hub and configure 3 more Quick links in order to have 6 active Quick links for current Time period.
        EXPECTED: 
        """
        pass

    def test_011_go_to_oxygen_application_event_hub_and_verify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application Event Hub and verify that 6 configured Quick links are displayed.
        EXPECTED: * Quick links container is displayed on Event Hub.
        EXPECTED: * Configured Quick links are displayed on Event Hub.
        EXPECTED: * 6 Quick links are displayed
        EXPECTED: **[CORAL]**:
        EXPECTED: * Quick links are displayed as 6 separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * Quick links that don't fit the width of the screen are cut off
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        """
        pass

    def test_012_click_anywhere__on_one_of_the_newly_configured_quick_linksverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere  on one of the newly configured quick links.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass
