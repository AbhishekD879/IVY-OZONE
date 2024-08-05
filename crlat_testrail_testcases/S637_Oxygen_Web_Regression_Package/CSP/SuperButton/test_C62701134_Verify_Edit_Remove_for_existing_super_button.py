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
class Test_C62701134_Verify_Edit_Remove_for_existing_super_button(Common):
    """
    TR_ID: C62701134
    NAME: Verify Edit/Remove for existing super button
    DESCRIPTION: This test case verifies Super button Updating
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

    def test_002_go_to_sports_pages_gt_super_button_gt_open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages &gt; Super Button &gt; open existing Super button
        EXPECTED: Super button details page is opened
        """
        pass

    def test_003_change_title_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Change title for existing Super button and save changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: Title of Super button is updated according to changes without page refresh
        """
        pass

    def test_005_load_cms_change_short_description_option_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change short description option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: Short Description of Super button is updated according to changes without page refresh
        """
        pass

    def test_007_load_cms_change_validity_period_startend_options_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change validity period start/end options for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: Validity period start/end of Super button is updated according to changes without page refresh
        """
        pass

    def test_009_load_cms_change_activeinactive_option_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change active/inactive option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: Data for Super button is NOT received from CMS if 'inactive' option is set up
        """
        pass

    def test_011_remove_existing_super_button_verify_in_application(self):
        """
        DESCRIPTION: Remove existing super button, verify in application
        EXPECTED: User should able to remove ,should be remove from application.
        """
        pass
