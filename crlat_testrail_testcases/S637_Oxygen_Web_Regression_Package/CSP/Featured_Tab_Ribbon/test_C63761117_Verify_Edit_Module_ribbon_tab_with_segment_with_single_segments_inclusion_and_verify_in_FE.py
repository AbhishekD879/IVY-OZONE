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
class Test_C63761117_Verify_Edit_Module_ribbon_tab_with_segment_with_single_segments_inclusion_and_verify_in_FE(Common):
    """
    TR_ID: C63761117
    NAME: Verify Edit Module ribbon tab with segment (with single segment(s) inclusion) and verify in FE
    DESCRIPTION: This test case verifies editing of existing Segment(s) inclusion Module ribbon tab
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

    def test_002_navigate_to_module_from_precondition_1(self):
        """
        DESCRIPTION: Navigate to module from precondition 1.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_module_ribbon_tab__link(self):
        """
        DESCRIPTION: Click on Module ribbon tab  link.
        EXPECTED: User should be able to view existing Module ribbon tab  should be displayed.
        """
        pass

    def test_004_click_on_existing_module_ribbon_tab__with_segment_inclusion(self):
        """
        DESCRIPTION: Click on existing Module ribbon tab  with segment inclusion
        EXPECTED: Module ribbon tab  detail page should be opened  with universal and segment(s) inclusion text box
        """
        pass

    def test_005_edit_existing_module_ribbon_tab(self):
        """
        DESCRIPTION: Edit existing Module ribbon tab
        EXPECTED: Add one segments in segment(s) inclusion text box
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: Module ribbon tab should be update successfully.
        """
        pass

    def test_007_load_oxygen_and_verify_module_ribbon_tab(self):
        """
        DESCRIPTION: Load oxygen and verify Module ribbon tab
        EXPECTED: Updated Module ribbon tab  should be shown for specific segmented user
        """
        pass
