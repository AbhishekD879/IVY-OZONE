import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C62903998_Verify_Featured_tab_module_module_ordering_for_specific_segments(Common):
    """
    TR_ID: C62903998
    NAME: Verify Featured tab module module ordering for specific segments
    DESCRIPTION: Test case verifies possibility to order Featured tab module module for specific segments
    PRECONDITIONS: **How to test in QA environment with prod campaign?**
    PRECONDITIONS: 1. Create a target group in Optimove prod env and build respective Campaign
    PRECONDITIONS: a. Optimove prod url https://lcg.optimove.net/#/
    PRECONDITIONS: 2. Create user(s) in QA env from sportsbook FE coral/Lads
    PRECONDITIONS: a. To create mass users in QA use this url https://localreports.ivycomptech.co.in/pls/trunkiappoker/p_r_acct_creation
    PRECONDITIONS: 3. Prepare CSV file with the users and campaign created in above steps
    PRECONDITIONS: a. Login_Name_Txt = username
    PRECONDITIONS: b. targetGroup = Campaign name
    PRECONDITIONS: 4. Upload CSV file in FTP location /home/digitalcrm
    PRECONDITIONS: 5. Invoke optimove data post API from the url http://qa2.api.bwin.com/v3/#crm-optimove-data-post
    PRECONDITIONS: a. AccessID = YWM5NDNjNWEtN2M0ZC00NjM4LWIwNWItNjFlMTllNzljY2Nh
    PRECONDITIONS: b. Campaign name = targetgroup name in CSV file
    PRECONDITIONS: c. "file": "/home/digitalcrm/XXXName.csv"
    PRECONDITIONS: 6. Create module in CMS with the campaign name in CSV e. super button 1 with segment name = campaign name in CSV.
    PRECONDITIONS: 7. Login with user(s) in CSV file we should able to see respective campaign data.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_featured_tab_module_link(self):
        """
        DESCRIPTION: click on Featured tab module link.
        EXPECTED: User should be able to view Already Created Featured tab modules should be displayed.
        """
        pass

    def test_004_verify_newly_created_featured_tab_modules_ordering_for_specific_segments(self):
        """
        DESCRIPTION: Verify newly created Featured tab modules ordering for specific segments
        EXPECTED: User should be able to view new configuration at the end of the list of existing specific-segments  after selecting the same specific segment from the dropdown.
        """
        pass

    def test_005_verify_if_content_manager_changes_segment_on_display(self):
        """
        DESCRIPTION: Verify if content manager changes segment on display
        EXPECTED: Segment dropdown list should show Universal and existing segment(s) one below the other in alphabetical order
        """
        pass

    def test_006_verify_the_order_of_the_featured_tab_module_module_for_specific_segments_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Featured tab module module for specific segments is as per order in the CMS.
        EXPECTED: The order is as defined in CMS.
        """
        pass

    def test_007_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated.
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
