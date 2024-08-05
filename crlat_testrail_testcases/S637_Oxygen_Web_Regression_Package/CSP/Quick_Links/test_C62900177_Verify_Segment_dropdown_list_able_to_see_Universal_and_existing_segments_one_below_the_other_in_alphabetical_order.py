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
class Test_C62900177_Verify_Segment_dropdown_list_able_to_see_Universal_and_existing_segments_one_below_the_other_in_alphabetical_order(Common):
    """
    TR_ID: C62900177
    NAME: Verify Segment dropdown list, able to see Universal and existing segments one below the other in alphabetical order.
    DESCRIPTION: This test case verifies order of in the segment dropdown list
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

    def test_004_click_on_segment_dropdown_and_verify_universal_segments_order(self):
        """
        DESCRIPTION: Click on segment dropdown and verify universal ,segments order
        EXPECTED: a) segment dropdown list should show Universal first and other segments should be in alphabetical order.
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: B) if user select any segment from drop down list the Quick linkss in that segment should display in alphabetical order.
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: C) If we remove all Quick linkss of any segment it should not display in drop down
        """
        pass
