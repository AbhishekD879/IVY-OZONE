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
class Test_C2553353_All_sports_Landing_pages_Expired_Quick_links(Common):
    """
    TR_ID: C2553353
    NAME: All sports Landing pages: Expired Quick links
    DESCRIPTION: This test case verifies expired Quick links on all sports Landing pages
    PRECONDITIONS: 1. Go to CMS -> Sport Pages-><Sport name>-> Quick Links and configure a Quick link for <Sport name> landing page with Validity period End Date=current time +10 minutes. - (<Quick Link1>)
    PRECONDITIONS: 2. There should be no other active Quick links for selected <Sport name> landing page expect <Quick Link1>.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to <Sport name> landing page.
    PRECONDITIONS: [Tab name]- This tab is selected by default after accessing Sport Landing Page. Name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
    PRECONDITIONS: Ladbrokes Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    PRECONDITIONS: Coral design (now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True

    def test_001_go_to_oxygen_app__sport_name_landing_page__tab_name_and_verify_that_configured_quick_link1_is_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that configured <Quick Link1> is displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is displayed.
        """
        pass

    def test_002_go_to_cms___sport_pages_sport_name__quick_links__and_create_the_second_active_quick_link_with_validity_period_end_datecurrent_time_plus20_minutes_quick_link2(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name>-> Quick Links  and create the second active Quick link with Validity period End Date=current time +20 minutes. (<Quick Link2>)
        EXPECTED: 
        """
        pass

    def test_003_go_to_oxygen_app__sport_name_landing_page__tab_name_and_verify_that_configured_quick_links_are_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that configured Quick links are displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick Links are displayed.
        """
        pass

    def test_004_wait_for_quick_link_from_step_2_to_get_expired_in_10_minutes(self):
        """
        DESCRIPTION: Wait for Quick link from Step 2 to get expired (in 10 minutes)
        EXPECTED: 
        """
        pass

    def test_005_go_to_oxygen_app__sport_name_landing_page__tab_name_and_verify_that_quick_link1_is_not_displayed_on_sport_name_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that <Quick Link1> is not displayed on <Sport name> landing page.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is not displayed.
        EXPECTED: * <Quick Link2> is displayed
        """
        pass

    def test_006_wait_for_quick_link1_to_get_expired_in_20_minutes(self):
        """
        DESCRIPTION: Wait for <Quick Link1> to get expired (in 20 minutes)
        EXPECTED: 
        """
        pass

    def test_007_go_to_oxygen_app__sport_name_landing_page__tab_name_and_verify_that_quick_link2_is_not_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Oxygen app-> <Sport name> landing page ->[Tab name] and verify that <Quick Link2> is not displayed on Homepage
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * No Quick links are displayed.
        """
        pass
