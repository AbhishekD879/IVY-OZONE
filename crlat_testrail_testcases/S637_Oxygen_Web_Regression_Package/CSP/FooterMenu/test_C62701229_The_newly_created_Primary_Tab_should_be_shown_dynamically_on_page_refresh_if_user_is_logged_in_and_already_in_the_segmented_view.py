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
class Test_C62701229_The_newly_created_Primary_Tab_should_be_shown_dynamically_on_page_refresh_if_user_is_logged_in_and_already_in_the_segmented_view(Common):
    """
    TR_ID: C62701229
    NAME: The newly created Primary Tab should be shown dynamically on page refresh if user is logged in and already in the segmented view.
    DESCRIPTION: This test case verifies newly created footer menu
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

    def test_001_launch_the_oxyzen_application_verify_existing_footer_menu(self):
        """
        DESCRIPTION: Launch the Oxyzen application ,Verify existing footer menu
        EXPECTED: Oxyzen application should launch successfully.Existing footer menu should be shown
        """
        pass

    def test_002_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_003_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_004_click_on_footer_menu_link(self):
        """
        DESCRIPTION: Click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_005_create_a_new_footer_menu(self):
        """
        DESCRIPTION: Create a new Footer menu
        EXPECTED: User should able to create new footer new
        """
        pass

    def test_006_goto_oxyzen_application_verify_newly_created_footer_menu(self):
        """
        DESCRIPTION: Goto Oxyzen application ,Verify newly created footer menu
        EXPECTED: Newly created footer menu should be shown dynamically upon refresh
        """
        pass
