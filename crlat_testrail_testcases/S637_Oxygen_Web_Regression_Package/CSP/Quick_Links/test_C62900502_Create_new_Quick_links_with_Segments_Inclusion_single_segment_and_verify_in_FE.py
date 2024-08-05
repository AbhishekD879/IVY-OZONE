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
class Test_C62900502_Create_new_Quick_links_with_Segments_Inclusion_single_segment_and_verify_in_FE(Common):
    """
    TR_ID: C62900502
    NAME: Create new Quick links with Segment(s) Inclusion (single segment) and verify in FE
    DESCRIPTION: This test case verifies creating a new Quick links with Segment(s) Inclusion (single segment)
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

    def test_003_click_on_quick_links_link(self):
        """
        DESCRIPTION: click on Quick links link.
        EXPECTED: User should be able to view existing Quick linkss should be displayed.
        """
        pass

    def test_004_click_on_quick_links_cta_button(self):
        """
        DESCRIPTION: Click on Quick links CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segment(s) inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select segment(s) inclusion radio button
        EXPECTED: Upon selecting Segment(s) inclusion button Segment(s) inclusion text box should be enabled.
        """
        pass

    def test_006_enter_segment_name_in_segments_inclusion_text_box_click_on_save_changes_button(self):
        """
        DESCRIPTION: Enter segment name in Segment(s) inclusion text box click on save changes button
        EXPECTED: Segmented Quick links should be created Successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_newly_created_quick_links_for_segmented_user(self):
        """
        DESCRIPTION: Load Oxygen app and verify newly created Quick links for segmented user
        EXPECTED: Specific segmented user only should able view newly created Quick links.
        EXPECTED: (Not visible in Universal view and other segmented view)
        """
        pass
