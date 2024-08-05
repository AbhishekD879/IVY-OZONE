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
class Test_C62903984_Verify_create_new_Featured_tab_module_by_Enhanced_Multiples_ID(Common):
    """
    TR_ID: C62903984
    NAME: Verify create new Featured tab module by Enhanced Multiples ID
    DESCRIPTION: This test case verifies the CMS configurations for Featured tab module with Enhanced Multiples ID
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
        EXPECTED: a) User should be able to view Create Featured tab module CTA.
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Existing Featured tab modules should be displayed.
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: c) Name,Segment(s),Segment(s) exclusion,Enabled,Display From,Display To,Channels,Personalized,Remove,Edit Columns should be displayed.
        """
        pass

    def test_006_click_on_create_featured_tab_module_with_enhanced_multiples_id(self):
        """
        DESCRIPTION: Click on create Featured tab module with Enhanced Multiples ID
        EXPECTED: User should able to create Featured module with Enhanced Multiples ID and appended at the end of the list of existing segment-specific configurations by default and allow reordering.
        """
        pass
