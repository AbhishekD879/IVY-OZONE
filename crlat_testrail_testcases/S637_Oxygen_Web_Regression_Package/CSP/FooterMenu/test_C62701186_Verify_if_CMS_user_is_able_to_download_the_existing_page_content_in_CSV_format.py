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
class Test_C62701186_Verify_if_CMS_user_is_able_to_download_the_existing_page_content_in_CSV_format(Common):
    """
    TR_ID: C62701186
    NAME: Verify if CMS user is able to download the existing page content in CSV format
    DESCRIPTION: This test case verifies allow to download existing page content in CSV format
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

    def test_002_go_to_menu__gt_footer_menues_page(self):
        """
        DESCRIPTION: Go to Menu -&gt; footer menues page
        EXPECTED: User should be able to see the Primary Tab Module page
        """
        pass

    def test_003_click_on_download_csv_cta_button(self):
        """
        DESCRIPTION: Click on "Download CSV" CTA button
        EXPECTED: Download CSV CTA button should be clickable,should able to download CSV file.
        """
        pass

    def test_004_verify_the_content_in_downloaded_file_csv_format(self):
        """
        DESCRIPTION: Verify the content in downloaded file CSV format
        EXPECTED: Downloaded CSV file content details should be correct.
        """
        pass
