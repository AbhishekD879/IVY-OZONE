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
class Test_C62701167_Verify_display_order_for_edited_super_button_in_segments(Common):
    """
    TR_ID: C62701167
    NAME: Verify display order for edited super button in segments
    DESCRIPTION: This test case verifies display order for edited super button in segments
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

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: Click on super button link.
        EXPECTED: User should be able to view existing super buttons should be displayed.
        """
        pass

    def test_004_click_on_existing_super_button_with_segment_inclusion(self):
        """
        DESCRIPTION: Click on existing super button with segment inclusion
        EXPECTED: super button detail page should be opened  with Segment(s)  inclusion radio button and segment(s) inclusion text box
        """
        pass

    def test_005_edit_existing_super_button(self):
        """
        DESCRIPTION: Edit existing super button
        EXPECTED: Add more than one segments in segment(s) inclusion text box
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: super button should be update successfully. Should navigate to super button module page
        """
        pass

    def test_007_verify_display_order_for_existing_and_newly_added_segment(self):
        """
        DESCRIPTION: Verify display order for existing and newly added segment
        EXPECTED: Segment belonged to existing before being edited, and the change was to newly add segment, the display order should not change for existing segments, but the configuration should display at the bottom of the list for newly added segment.
        """
        pass
