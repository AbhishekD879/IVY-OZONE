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
class Test_C62162655_Verify_recently_played_games_removal_based_on_user_risk_level_at_medium_high_very_high(Common):
    """
    TR_ID: C62162655
    NAME: Verify recently played games removal based on user risk level at medium ,high, very high
    DESCRIPTION: The Test case verifies Recently played games  removal for risk level Users
    PRECONDITIONS: "Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_medium_tbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Medium ,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_medium_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as medium risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_003_verify_recent_played_games_are_appear(self):
        """
        DESCRIPTION: Verify Recent Played games are appear
        EXPECTED: Recent Played games removed for all sports
        """
        pass

    def test_004_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_005_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_hightbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as HIGH,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_006_login_into_oxygen_application_as_high_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as High risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_007_verify_recent_played_games_are_removed(self):
        """
        DESCRIPTION: Verify Recent Played games are removed
        EXPECTED: Recent Played games removed for all sports
        """
        pass

    def test_008_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_009_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_very_high_tbd_respectively(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Very High ,TBD respectively
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_010_login_into_oxygen_application_as_vhigh_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as V.High risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_011_verify_recent_played_games__are_removed(self):
        """
        DESCRIPTION: Verify Recent Played games  are removed
        EXPECTED: Recent Played games removed for all sports
        """
        pass
