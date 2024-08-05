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
class Test_C62701198_Verify_Footer_menu_module_ordering_for_specific_segments(Common):
    """
    TR_ID: C62701198
    NAME: Verify Footer menu module ordering for specific segments
    DESCRIPTION: Test case verifies possibility to order Footer menu. module for specific segements
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

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_004_verify_newly_created_footer_menus_ordering_for_specific_segements(self):
        """
        DESCRIPTION: Verify newly created Footer Menus ordering for specific segements
        EXPECTED: User should be able to view new configuration at the end of the list of existing specific-segments  after selecting the same specific segment from the dropdown.
        """
        pass

    def test_005_verify_if_content_manager_changes_segment_on_display(self):
        """
        DESCRIPTION: Verify if content manager changes segment on display
        EXPECTED: Segment dropdown list should show Universal and existing segment(s) one below the other in alphabetical order
        """
        pass

    def test_006_verify_the_order_of_the_footer_menu_module_for_specific_segements_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Footer Menu module for specific segements is as per order in the CMS.
        EXPECTED: The order is as defined in CMS.
        """
        pass

    def test_007_reorder_by_drag_and_drop_in_cms_and_verify_the_order_in_fe(self):
        """
        DESCRIPTION: Reorder by drag and drop in CMS and verify the order in FE
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
