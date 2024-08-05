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
class Test_C62701141_Verify_super_button_module_ordering_for_universal(Common):
    """
    TR_ID: C62701141
    NAME: Verify super button module ordering for universal
    DESCRIPTION: Test case verifies possibility to order super button module for Universal
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

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on super button link.
        EXPECTED: User should be able to view Already Created super buttons should be displayed.
        """
        pass

    def test_004_verify_newly_created_super_buttons_ordering(self):
        """
        DESCRIPTION: Verify newly created super buttons ordering
        EXPECTED: User should be able to view new configuration at the end of the list of existing segment-specific configurations by default.
        """
        pass

    def test_005_verify_the_order_of_the_super_button_module_for_universal_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the super button module for universal is as per order in the CMS.
        EXPECTED: The order is as defined in CMS.
        """
        pass

    def test_006_change_the_order_by_drag_and_drop_in_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order by drag and drop in CMS .In the application refresh the page and verify the order is updated.
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
