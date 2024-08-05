import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62167416_Verify_gaming_carousel_banners_removal_for_user_risk_level_at_very_High(Common):
    """
    TR_ID: C62167416
    NAME: Verify gaming carousel banners removal for user risk level at very High
    DESCRIPTION: The test case verifies banner removed for risk level Users
    PRECONDITIONS: "Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerhigh_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,HIGH ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_high_risk_user_gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as HIGH risk User-&gt; go to home Page
        EXPECTED: User logged in succesfully
        """
        pass

    def test_003_verify_gaming_corousel_banners_are_remove_or_not_in_homepage(self):
        """
        DESCRIPTION: Verify gaming corousel banners are remove or not in homepage
        EXPECTED: All gaming carousel banners removed for all sports
        """
        pass

    def test_004_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass
