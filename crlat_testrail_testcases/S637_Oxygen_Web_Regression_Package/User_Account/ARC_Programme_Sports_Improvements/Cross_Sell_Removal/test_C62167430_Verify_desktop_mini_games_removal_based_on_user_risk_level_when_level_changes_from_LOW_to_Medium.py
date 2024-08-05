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
class Test_C62167430_Verify_desktop_mini_games_removal_based_on_user_risk_level_when_level_changes_from_LOW_to_Medium(Common):
    """
    TR_ID: C62167430
    NAME: Verify desktop mini games removal based on user risk level when level changes from LOW to Medium
    DESCRIPTION: The test case verifies mini games removed for risk level Users
    PRECONDITIONS: "Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_lowtbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Low,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_high_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as High risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_003_verify_desktop_minigames_are_appear(self):
        """
        DESCRIPTION: Verify desktop minigames are appear
        EXPECTED: Mini games appeared for all sports
        """
        pass

    def test_004_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_changes_from_low_to_high_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level changes from LOW to HIGH ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_005_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_006_login_again_into_oxygen_application_as_high_risk_user__gtgt_check_minigames_removed_for_all_sports_on_new_session(self):
        """
        DESCRIPTION: Login again into Oxygen application as HIGH risk user -&gt;&gt; check minigames removed for all Sports on new session
        EXPECTED: Minigames removed for all sports
        """
        pass
