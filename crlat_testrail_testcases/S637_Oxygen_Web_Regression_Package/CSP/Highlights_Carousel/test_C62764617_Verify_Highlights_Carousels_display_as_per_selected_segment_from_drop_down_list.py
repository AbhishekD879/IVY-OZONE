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
class Test_C62764617_Verify_Highlights_Carousels_display_as_per_selected_segment_from_drop_down_list(Common):
    """
    TR_ID: C62764617
    NAME: Verify Highlights Carousels display as per selected segment from drop down list
    DESCRIPTION: This test case verifies segment dropdown functionality on Highlights Carousel module page.
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
        EXPECTED: User should be able to view the Highlights Carousel Module page
        """
        pass

    def test_003_verify_highlights_carousel_page(self):
        """
        DESCRIPTION: Verify Highlights Carousel page
        EXPECTED: The Highlights Carousel Module page as per the designs below
        EXPECTED: Create Highlights Carousel,  Segment, Download CSV , Search field
        """
        pass

    def test_004_verify_segment_dropdown_by_selecting_specific_segment(self):
        """
        DESCRIPTION: Verify Segment dropdown by selecting specific segment
        EXPECTED: The dropdown will show segmented records
        EXPECTED: Note- When user is performing search, how we are going to display the table- Search operation will basically return search result from the segment data which is selected in segment dropdown.
        """
        pass
