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
class Test_C62167431_Verify_recently_played_games_not_removal_based_on_user_risk_level_when_level_changes_from_HIGH_to_LOW(Common):
    """
    TR_ID: C62167431
    NAME: Verify recently played games not removal based on user risk level when level changes from HIGH to LOW
    DESCRIPTION: The test case verifies Recently played games removed for risk level Users
    PRECONDITIONS: "Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_high_tbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as HIGH ,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_high_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as High risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_003_verify_recently_played_games_are_removed(self):
        """
        DESCRIPTION: Verify recently played games are removed
        EXPECTED: recently played games removed for all sports
        """
        pass

    def test_004_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_changes_from_high_to_low_tbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level changes from HIGH to LOW ,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_005_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_006_login_again_into_oxygen_application_as_low_risk_user__gtgt_check_recently_played_games_are_removed_for_all_sports_on_new_session(self):
        """
        DESCRIPTION: Login again into Oxygen application as Low risk user -&gt;&gt; check recently played games are removed for all Sports on new session
        EXPECTED: recently played games NOT removed for all sports
        """
        pass
