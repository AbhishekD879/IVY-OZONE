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
class Test_C62764783_Verify_Edit_Remove_should_be_disabled_for_records_other_than_selected_segment_in_the_dropdownin_detail_view_as_well(Common):
    """
    TR_ID: C62764783
    NAME: Verify Edit/Remove should be disabled for records other than selected segment in the dropdown(in detail view as well)
    DESCRIPTION: This test case verifies edit/remove buttons should be disabled other than the selected segment in the drop down (in details view as well)
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

    def test_003_click_on_surface_bet_link(self):
        """
        DESCRIPTION: Click on surface bet link.
        EXPECTED: User should be able to view existing surface bets should be displayed.
        """
        pass

    def test_004_select_one_of_the_segment_dropdown_and_verify_editremove_button_for_only_selected_segment_on_surface_bets_page(self):
        """
        DESCRIPTION: Select one of the segment dropdown, and verify Edit/remove button for only selected segment on surface bets' Page
        EXPECTED: User should able to select from the segment drop down. Edit/Remove button should be enabled for only selected segment on surface bets' Page
        """
        pass

    def test_005_navigate_to_surface_bet_detail_page_of_selected_segment(self):
        """
        DESCRIPTION: Navigate to surface bet detail page of selected segment
        EXPECTED: Edit/Remove button should be enable for only selected segment, should allow to edit/remove in detail view
        """
        pass
