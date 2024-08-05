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
class Test_C62701190_The_new_configuration_will_be_appended_at_the_end_of_the_list_of_existing_segment_Universal_specific_configurations_by_default_and_allow_reordering(Common):
    """
    TR_ID: C62701190
    NAME: The new configuration will be appended at the end of the list of existing segment-Universal/specific configurations by default and allow reordering.
    DESCRIPTION: This test case verifies the newly configured will be appended at the end of the list of existing Universal/segment-specific configurations by default and allow reordering.
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

    def test_001_verify_newly_created_footer_menu(self):
        """
        DESCRIPTION: Verify newly created footer menu
        EXPECTED: User should be able to view new configuration at the end of the list of existing Universal/segment-specific configurations by default.
        """
        pass

    def test_002_verify_drag_and_drop_for_reordering(self):
        """
        DESCRIPTION: Verify drag and drop for reordering
        EXPECTED: User should able to drag and drop for reorder for universal and Segment list.
        """
        pass
