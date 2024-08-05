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
class Test_C62701188_Verify_create_new_footer_menu_primary_tab_functionality(Common):
    """
    TR_ID: C62701188
    NAME: Verify create new footer menu (primary tab) functionality
    DESCRIPTION: This test case verifies the CMS configurations for footer menu (primary tab)
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

    def test_002_go_to_menu_gt_footer_menus(self):
        """
        DESCRIPTION: Go to Menu &gt; footer menus
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_footermenu_link(self):
        """
        DESCRIPTION: Click on FooterMenu link
        EXPECTED: Existing footer menus should be displayed.
        """
        pass

    def test_004_verify_create_footer_menu_page(self):
        """
        DESCRIPTION: Verify Create Footer menu page
        EXPECTED: a) User should be able to view Create FooterMenu CTA.
        EXPECTED: b)Upon clicking Create FooterMenu CTA, Link Tiltle, Traget URI pop up should display with Save and Close buttons
        """
        pass

    def test_005_verify_detail_configuration_for_footer_menu(self):
        """
        DESCRIPTION: Verify detail configuration for footer menu
        EXPECTED: Configuration page should be opened with below feilds
        EXPECTED: Link Title,Target Uri,Show Item For,System ID,SVG Icon,Filename and new radio buttons Universal ,Segment(s) inclusion with save changes,Revert changes and remove options.
        """
        pass

    def test_006_verify_by_entering__all_mandatory_fields_and_click_save__changes_cta(self):
        """
        DESCRIPTION: Verify by entering  all mandatory fields and click Save  Changes CTA
        EXPECTED: Upon Clicking Save Changes CTA , new Footer menu should be created and appended at the end of the list of existing segment-specific configurations by default and allow reordering.
        """
        pass
