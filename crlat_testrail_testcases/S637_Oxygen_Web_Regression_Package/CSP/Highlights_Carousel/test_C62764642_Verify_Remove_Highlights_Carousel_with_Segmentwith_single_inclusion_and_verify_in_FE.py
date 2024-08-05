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
class Test_C62764642_Verify_Remove_Highlights_Carousel_with_Segmentwith_single_inclusion_and_verify_in_FE(Common):
    """
    TR_ID: C62764642
    NAME: Verify Remove Highlights Carousel with Segment(with single inclusion) and verify in FE
    DESCRIPTION: This test case verifies removal Segment(with single inclusion)
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

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_highlights_carousel_link(self):
        """
        DESCRIPTION: Click on Highlights Carousel link.
        EXPECTED: User should be able to view existing Highlights Carousels should be displayed.
        """
        pass

    def test_004_click_on_existing_highlights_carousel_with_segmentwith_single_inclusion(self):
        """
        DESCRIPTION: Click on existing Highlights Carousel with Segment(with single inclusion)
        EXPECTED: Highlights Carousel detail page should be opened  with Universal (with single exclusion)
        """
        pass

    def test_005_click_on_remove_button(self):
        """
        DESCRIPTION: Click on Remove button
        EXPECTED: Highlights Carousel should be removed successfully
        """
        pass

    def test_006_load_oxygen_and_verify_highlights_carousel(self):
        """
        DESCRIPTION: Load oxygen and verify Highlights Carousel
        EXPECTED: Removed Highlights Carousel should not be shown in application, Highlights Carousel should be removed from specific segment
        """
        pass
