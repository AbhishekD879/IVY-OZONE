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
class Test_C62162656_Verify_Gaming_overlay_removal_based_on_user_risk_level_at_medium_high_very_high(Common):
    """
    TR_ID: C62162656
    NAME: Verify Gaming overlay removal  based on user risk level at medium ,high, very high
    DESCRIPTION: The Test case verifies gaming Overlay removal for risk level Users
    PRECONDITIONS: "Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: The user demographics details such as Model and Risk Level, MoH, frequency inputs are provided by the platform.
    PRECONDITIONS: All user Interaction will be captured by system.
    PRECONDITIONS: Change of user behavior will be performed only on new session.
    PRECONDITIONS: The features such as Messaging others are configurable in the CMS or Sitecore (TBC: Technology)"
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_medium_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Medium ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_medium_risk_user__(self):
        """
        DESCRIPTION: Login into Oxygen Application as medium risk User -
        EXPECTED: User logged in successfully
        """
        pass

    def test_003_verify_gaming_overlay__are_appear__switchoff_in_mobile_web(self):
        """
        DESCRIPTION: Verify gaming Overlay  are appear [ SwitchOFF in mobile Web]
        EXPECTED: gaming Overlay  removed for all sports and user should redirected to Lobby
        """
        pass

    def test_004_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_005_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_hightbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as HIGH,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_006_login_into_oxygen_application_as_high_risk_user(self):
        """
        DESCRIPTION: Login into Oxygen Application as High risk User
        EXPECTED: User logged in successfully
        """
        pass

    def test_007_click_on_gaming_menu_in_sports_ribbon(self):
        """
        DESCRIPTION: Click on Gaming menu in Sports Ribbon
        EXPECTED: "User is directed to Gaming menu /Lobby
        EXPECTED: No Overlay is displayed"
        """
        pass

    def test_008_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out successfully from Oxygen site
        """
        pass

    def test_009_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblerrisk_level_as_very_high_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Risk Level as Very High ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_010_login_into_oxygen_application_as_vhigh_risk_user__gt_go_to_home_page(self):
        """
        DESCRIPTION: Login into Oxygen Application as V.High risk User -&gt; go to home Page
        EXPECTED: User logged in successfully
        """
        pass

    def test_011_click_on_gaming_menu_in_sports_ribbon(self):
        """
        DESCRIPTION: Click on Gaming menu in Sports Ribbon
        EXPECTED: "User is directed to Gaming menu /Lobby
        EXPECTED: No Overlay is displayed"
        """
        pass
