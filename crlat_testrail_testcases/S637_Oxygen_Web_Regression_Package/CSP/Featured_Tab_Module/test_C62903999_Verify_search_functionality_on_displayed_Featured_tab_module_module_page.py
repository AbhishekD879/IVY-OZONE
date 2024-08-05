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
class Test_C62903999_Verify_search_functionality_on_displayed_Featured_tab_module_module_page(Common):
    """
    TR_ID: C62903999
    NAME: Verify search functionality on displayed Featured tab module module page.
    DESCRIPTION: This test case verifies search functionality by text in the records shown on the table in Featured tab module module page.
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
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to view the Featured tab module Module page
        """
        pass

    def test_003_click_at_search_for_featured_tab_module(self):
        """
        DESCRIPTION: Click at "Search for Featured tab module"
        EXPECTED: User should able to click and able to enter text
        """
        pass

    def test_004_search_by_link_tittle(self):
        """
        DESCRIPTION: Search by link tittle
        EXPECTED: a) Should able to search by Link tittle, all related records should be shown
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: b) results should retain from selected drop down only which means if user select any segment search should not display Featured tab modules in other segment
        """
        pass
