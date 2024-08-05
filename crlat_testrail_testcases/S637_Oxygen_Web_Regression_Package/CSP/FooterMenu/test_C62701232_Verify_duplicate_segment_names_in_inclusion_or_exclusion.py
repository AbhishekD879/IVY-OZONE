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
class Test_C62701232_Verify_duplicate_segment_names_in_inclusion_or_exclusion(Common):
    """
    TR_ID: C62701232
    NAME: Verify duplicate segment names in inclusion or exclusion
    DESCRIPTION: This test case verifies duplicates segment names in inclusion or exclusion
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

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: Click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_004_click_on_create_footer_menu_cta_button(self):
        """
        DESCRIPTION: Click on Create Footer Menu CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segment(s) inclusion with text boxes
        """
        pass

    def test_005_select_universalradio_button(self):
        """
        DESCRIPTION: Select Universalradio button
        EXPECTED: Upon selecting universal radio button Segment(s) exclusion text box should be enabled.
        """
        pass

    def test_006_enter_duplicate_segment_names_in_segments_exclusion_text_box(self):
        """
        DESCRIPTION: Enter duplicate segment names in segment(s) Exclusion text box
        EXPECTED: Duplicate segment names should allowed
        EXPECTED: Content user has to make sure to configure correct segment names as in optimove
        """
        pass

    def test_007_edit_exisiting_universal_footer_menu_with_duplicate_segments_name(self):
        """
        DESCRIPTION: Edit exisiting Universal Footer menu with duplicate segments name
        EXPECTED: Duplicate segment names should allowed
        EXPECTED: Content user has to make sure to configure correct segment names as in optimove
        """
        pass

    def test_008_repeat_same_steps_for_segments_inclusion(self):
        """
        DESCRIPTION: Repeat same steps for Segment(s) inclusion
        EXPECTED: Duplicate segment names should allowed
        EXPECTED: Content user has to make sure to configure correct segment names as in optimove
        """
        pass
