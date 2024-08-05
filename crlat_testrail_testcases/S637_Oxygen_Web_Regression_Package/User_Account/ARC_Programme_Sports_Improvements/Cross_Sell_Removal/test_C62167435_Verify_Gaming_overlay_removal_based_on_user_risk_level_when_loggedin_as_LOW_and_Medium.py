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
class Test_C62167435_Verify_Gaming_overlay_removal_based_on_user_risk_level_when_loggedin_as_LOW_and_Medium(Common):
    """
    TR_ID: C62167435
    NAME: Verify Gaming overlay removal based on user risk level when loggedin as  LOW and Medium
    DESCRIPTION: The test case verifies gaming Overlay removed for risk level Users
    PRECONDITIONS: "System Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    PRECONDITIONS: QA Pre-requisite : NO
    PRECONDITIONS: Note: Pre Setup is not required to setup by QA team for this scenario
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_lowtbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Low,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_low_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as LOW risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_003_click_on_gaming_menu_in_sports_ribbon(self):
        """
        DESCRIPTION: Click on Gaming menu in Sports Ribbon
        EXPECTED: "Gaming Overlay is displayed to the User
        EXPECTED: Close icon is displayed at Top Right Corner
        EXPECTED: Go To Gaming Home Page button is displayed at the botton
        EXPECTED: On Clicking Close Icon User is redirected to Sports Home page"
        """
        pass

    def test_004_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_medium_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as MEDIUM ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_005_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_006_login_again_into_oxygen_application_as_high_risk_user__gtgt_check_gaming_overlay_removed_for_all_sports_on_new_session_switchoff_in_mobile_web(self):
        """
        DESCRIPTION: Login again into Oxygen application as HIGH risk user -&gt;&gt; check gaming overlay removed for all Sports on new session[ SwitchOFF in mobile Web]
        EXPECTED: user should redirected to Lobby
        """
        pass

    def test_007_click_on_gaming_menu_in_sports_ribbon(self):
        """
        DESCRIPTION: Click on Gaming menu in Sports Ribbon
        EXPECTED: "User is directed to Gaming menu /Lobby
        EXPECTED: No Overlay is displayed"
        """
        pass
