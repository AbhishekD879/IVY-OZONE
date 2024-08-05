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
class Test_C62903991_Verify_segmented_view_for_segmented_user(Common):
    """
    TR_ID: C62903991
    NAME: Verify segmented view for segmented user
    DESCRIPTION: This test case verifies segmented view for segmented user
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

    def test_001_launch_the_application_in_mobile(self):
        """
        DESCRIPTION: Launch the application in mobile
        EXPECTED: Application should launch successfully.
        """
        pass

    def test_002_login_with_specific_segmented_user(self):
        """
        DESCRIPTION: Login with specific segmented user
        EXPECTED: User should login successfully
        """
        pass

    def test_003_verify_segmented_view(self):
        """
        DESCRIPTION: Verify segmented view
        EXPECTED: User should able to see segmented view for specific segmented user.(Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
        """
        pass

    def test_004_repeat_for_all_types_of_segmented_users(self):
        """
        DESCRIPTION: Repeat for all types of segmented users
        EXPECTED: User should able to see other segmented view for other segmented users(Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
        """
        pass
