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
class Test_C9726398_Event_hub_Verify_adding_removing_Quick_links_on_Event_Hub(Common):
    """
    TR_ID: C9726398
    NAME: Event hub: Verify adding/removing Quick links on Event Hub
    DESCRIPTION: This test case verifies adding of Quick links to Event hub
    PRECONDITIONS: 1. Event Hub is configured in CMS > Sport Pages > Event hub
    PRECONDITIONS: 2. There should be no active Quick links for Event hub in CMS
    PRECONDITIONS: 3. Go to Oxygen app and navigate to Event hub tab.
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_quick_link_container(self):
        """
        DESCRIPTION: Verify displaying of Quick link container
        EXPECTED: * Quick links container is not displayed
        EXPECTED: * No Quick Links are displayed
        """
        pass

    def test_002_go_to_cms___sport_pages_event_hub___quick_links_and_configure_one_quick_link(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Event Hub -> Quick Links and configure one Quick Link
        EXPECTED: 
        """
        pass

    def test_003_go_to_oxygen_application_and_navigate_to_event_hub_tabverify_that_configured_quick_link_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application and navigate to Event hub tab.
        DESCRIPTION: Verify that configured Quick link is displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed in Feature tab on Homepage.
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        pass

    def test_004_click_anywhere_on_the_quick_linkverify_redirection_to_url_previously_configured_in_cms_within_the_application(self):
        """
        DESCRIPTION: Click anywhere on the quick link
        DESCRIPTION: Verify redirection to URL previously configured in CMS within the application
        EXPECTED: * User is redirected to specific page(URL) previously configured in Quick link CMS configuration.
        EXPECTED: * Page is opened within the application.
        """
        pass

    def test_005_select_any_other_tab_on_homepagein_play_coupons_next_races_build_your_bet_etcverify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on Homepage(In-Play, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of Quick links on other tabs.
        EXPECTED: * Configured Quick links are displayed only on Event hub from preconditions.
        EXPECTED: * Quick links container is NOT displayed on other Homepage  tabs.
        EXPECTED: * Configured Quick links are NOT displayed on other Homepage tabs.
        """
        pass

    def test_006_go_to_any_sport_page_eg_football_tennis_and_observe_quick_links_sectionverify_displaying_of_event_hub_configured_quick_link_on_any_sport_landing_page(self):
        """
        DESCRIPTION: Go to any Sport page (e.g. Football, Tennis) and observe Quick links section.
        DESCRIPTION: Verify displaying of Event hub configured Quick link on any Sport landing page
        EXPECTED: * Configured Quick link for Event hub is not displayed on other Sport pages.
        EXPECTED: **Only quick links that are configured for Sport landing page are shown (if there are any).
        EXPECTED: **Quick links container and links are not displayed If no quick links are configured for Sport pages.
        """
        pass

    def test_007_go_to_cms___sport_pages_event_hub___quick_links_and_set_active_inactive_flag_for_configured_quick_link_for_event_hub_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Event hub -> Quick Links and set "Active/ Inactive" flag for configured quick link for Event hub to 'Inactive'.
        EXPECTED: 
        """
        pass

    def test_008_go_to_oxygen_app_and_navigate_to_event_hub_tab_on_homepageverify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event hub tab on Homepage.
        DESCRIPTION: Verify that Quick link is no longer displayed.
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * Quick link is no longer displayed.
        """
        pass

    def test_009_go_to_cms___sport_pages_event_hub___quick_links_and_set_active_inactive_flag_for_configured_quick_link_for_homepage_to_active(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Event hub -> Quick Links and set "Active/ Inactive" flag for configured quick link for Homepage to 'Active'.
        EXPECTED: 
        """
        pass

    def test_010_go_to_oxygen_app_and_navigate_to_event_hub_on_homepageverify_that_quick_link_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event hub on Homepage.
        DESCRIPTION: Verify that Quick link is displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed on Homepage.
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        pass

    def test_011_go_to_cms___sport_pages_event_hub___quick_links_and_remove_previously_created_quick_link(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Event hub -> Quick Links and remove previously created Quick link
        EXPECTED: 
        """
        pass

    def test_012_go_to_oxygen_app_and_navigate_to_event_hub_tab_on_homepageverify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event hub tab on Homepage.
        DESCRIPTION: Verify that Quick link is no longer displayed.
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * Quick link is no longer displayed.
        """
        pass
