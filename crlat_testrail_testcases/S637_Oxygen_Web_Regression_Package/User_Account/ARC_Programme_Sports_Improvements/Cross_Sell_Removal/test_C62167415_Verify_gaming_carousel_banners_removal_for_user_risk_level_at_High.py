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
class Test_C62167415_Verify_gaming_carousel_banners_removal_for_user_risk_level_at_High(Common):
    """
    TR_ID: C62167415
    NAME: Verify gaming carousel banners removal for user risk level at High
    DESCRIPTION: The test case verifies banner removed for risk level Users
    PRECONDITIONS: For the following User Risk and reason code Carousal banners should NOT be displayed
    PRECONDITIONS: "3.9", "3.10", "3.15", "3.500", "4.3", "4.9", "4.10", "4.15", "4.500", "4.600", "4.601", "4.602", "4.603", "4.604", "5.3", "5.9", "5.10", "5.15", "5.501", "5.502", "5.503", "5.600", "5.601", "5.602", "5.603", "5.604"
    PRECONDITIONS: For banners ARC rules are configured in Site Core
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_login_as_content_user_and_configure_model_risk_moh_fields_as_problem_gamblervery_high_tbd_respectivley(self):
        """
        DESCRIPTION: Go to CMS and login as Content User and configure Model &Risk &MOH fields as Problem Gambler,Very High ,TBD respectivley
        EXPECTED: CMS configuration done with all changes.
        """
        pass

    def test_002_login_into_oxygen_application_as_high_risk_user_with_reason_codes_as_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Login into Oxygen Application as High risk User with reason codes as mentioned in Pre-Conditions
        EXPECTED: User logged in succesfully
        """
        pass

    def test_003_verify_gaming_corousel_banners_are_remove_or_not_in_homepagebanners_for_which_arc_rules_are_configured_in_site_core(self):
        """
        DESCRIPTION: Verify gaming corousel banners are remove or not in homepage
        DESCRIPTION: Banners for which ARC rules are configured in site core
        EXPECTED: All gaming carousel banners removed for all sports
        """
        pass

    def test_004_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen Application
        EXPECTED: User logged out succesfully from Oxygen site
        """
        pass
