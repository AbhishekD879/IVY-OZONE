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
class Test_C62167422_Verify_gaming_carousel_banners_removal_on_new_session_when_user_login_with_risk_level_LOW_to_Medium(Common):
    """
    TR_ID: C62167422
    NAME: Verify gaming carousel banners removal on new session when user login with risk level  LOW to Medium
    DESCRIPTION: The test case verifies banner removed for risk level Users
    PRECONDITIONS: For the following User Risk and reason code Carousal banners should NOT be displayed
    PRECONDITIONS: "3.9", "3.10", "3.15", "3.500", "4.3", "4.9", "4.10", "4.15", "4.500", "4.600", "4.601", "4.602", "4.603", "4.604", "5.3", "5.9", "5.10", "5.15", "5.501", "5.502", "5.503", "5.600", "5.601", "5.602", "5.603", "5.604"
    PRECONDITIONS: For banners ARC rules are configured in Site Core
    """
    keep_browser_open = True

    def test_001_login_as_low_risk_user_profile_not_from_the_pre_conditions(self):
        """
        DESCRIPTION: Login as LOW risk User (Profile not from the pre-conditions)
        EXPECTED: User logged in successfully
        """
        pass

    def test_002_verify_gaming_carousel_bannersbanners_for_which_arc_rules_are_configured_in_site_core(self):
        """
        DESCRIPTION: Verify gaming carousel banners
        DESCRIPTION: Banners for which ARC rules are configured in site core
        EXPECTED: All banners including the banners with ARC configurations are displayed to the User
        """
        pass

    def test_003_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User should be able to Logout
        """
        pass

    def test_004_re_login_with_medium_arc_user(self):
        """
        DESCRIPTION: Re-Login with medium arc user
        EXPECTED: Banners with ARC configurations in Site core should not be displayed to the user
        """
        pass
