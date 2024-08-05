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
class Test_C62701233_Verify_segmented_view_for_specific_exTennis_segmented_user_with_universal_excluded_other_then_tennis(Common):
    """
    TR_ID: C62701233
    NAME: Verify segmented view for specific (ex:Tennis )segmented user with universal excluded (other then tennis)
    DESCRIPTION: This test case verifies segmented view for specific (ex:Tennis ) segmented user with universal excluded (other then tennis)
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

    def test_001_launch_oxygen_application_and_login_with_segmented_user_extennis(self):
        """
        DESCRIPTION: Launch oxygen application and login with segmented user (ex:Tennis)
        EXPECTED: User should able to launch and login successfully
        """
        pass

    def test_002_verify_segmented_view_for_logged_in_user_extennis_(self):
        """
        DESCRIPTION: Verify segmented view for logged in user (ex:tennis )
        EXPECTED: User should able to view segmented and Universal along with Universal footer menu segment(s) exclusion (ex:other then Tennis)
        """
        pass

    def test_003_login_in_fe_with_segmented_userwhich_is_configured_in_segments_exclusion_text_box_cms(self):
        """
        DESCRIPTION: Login in FE with segmented user,which is configured in segment(s) exclusion text box (CMS)
        EXPECTED: User should able view segmented and Universal without Universal footer menu segment(s) exclusion
        """
        pass
