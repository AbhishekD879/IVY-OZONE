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
class Test_C62904015_Create_new_Featured_tab_module_with_Segments_Inclusion_Multiple_segment_names_and_verify_in_FE(Common):
    """
    TR_ID: C62904015
    NAME: Create new Featured tab module with Segment(s) Inclusion (Multiple segment names) and verify in FE
    DESCRIPTION: This test case verifies creating a new Featured tab module with Segment(s) Inclusion (Multiple segment names)
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
        EXPECTED: User should be able to view existing Featured tab module should be displayed.
        """
        pass

    def test_004_click_on_create_featured_tab_module_cta_button(self):
        """
        DESCRIPTION: Click on Create Featured tab module CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segment(s) inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select segment(s) inclusion radio button
        EXPECTED: Upon selecting universal radio button Segment(s) inclusion text box should be enabled.
        """
        pass

    def test_006_enter_more_than_one_segment_name_in_segments_inclusion_text_box_with_comma_separated_click_on_save_changes_button(self):
        """
        DESCRIPTION: Enter more than one segment name in Segment(s) inclusion text box with comma separated, click on save changes button
        EXPECTED: Segmented Featured tab module should be created Successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_newly_created_featured_tab_module(self):
        """
        DESCRIPTION: Load Oxygen app and verify newly created Featured tab module
        EXPECTED: Specific segmented users only should able view newly created Featured tab module.
        EXPECTED: (Not visible in Universal view and other segmented view)
        """
        pass
