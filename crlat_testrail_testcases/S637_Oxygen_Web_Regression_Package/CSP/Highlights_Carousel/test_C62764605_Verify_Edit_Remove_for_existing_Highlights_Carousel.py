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
class Test_C62764605_Verify_Edit_Remove_for_existing_Highlights_Carousel(Common):
    """
    TR_ID: C62764605
    NAME: Verify Edit/Remove for existing Highlights Carousel
    DESCRIPTION: This test case verifies Highlights Carousel Updating
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

    def test_002_go_to_sports_pages_gt_highlights_carousel_gt_open_existing_highlights_carousel(self):
        """
        DESCRIPTION: Go to Sports Pages &gt; Highlights Carousel &gt; open existing Highlights Carousel
        EXPECTED: Highlights Carousel details page is opened
        """
        pass

    def test_003_change_title_for_existing_highlights_carousel_and_save_changes(self):
        """
        DESCRIPTION: Change title for existing Highlights Carousel and save changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_load_oxygen_app_go_to_the_page_where_highlights_carousel_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Highlights Carousel is set up
        EXPECTED: Title of Highlights Carousel is updated according to changes without page refresh
        """
        pass

    def test_005_load_cms_change_svg_icon_option_for_existing_highlight_carousel__and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change SVG icon option for existing Highlight carousel  and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_go_to_the_page_where_highlight_carousel_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Highlight carousel is set up
        EXPECTED: SVG icon option for existing Highlight carousel  is updated according to changes without page refresh
        """
        pass

    def test_007_load_cms_change_display_fromto_options_for_existing_highlights_carousel_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change Display from/to options for existing Highlights Carousel and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_load_oxygen_app_go_to_the_page_where_highlights_carousel_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Highlights Carousel is set up
        EXPECTED: Display from/to of Highlights Carousel is updated according to changes without page refresh
        """
        pass

    def test_009_load_cms_change_activeinactive_option_for_existing_highlights_carousel_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change active/inactive option for existing Highlights Carousel and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010_load_oxygen_app_go_to_the_page_where_highlights_carousel_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Highlights Carousel is set up
        EXPECTED: Data for Highlights Carousel is NOT received from CMS if 'inactive' option is set up
        """
        pass

    def test_011_remove_existing_highlights_carousel_verify_in_application(self):
        """
        DESCRIPTION: Remove existing Highlights Carousel, verify in application
        EXPECTED: User should able to remove ,should be remove from application.
        """
        pass
