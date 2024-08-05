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
class Test_C62167414_Verify_gaming_carousel_banners_not_removal_on_new_session_when_user_login_with_risk_level_High_to_LOW(Common):
    """
    TR_ID: C62167414
    NAME: Verify gaming carousel banners not removal on new session when user login with risk level  High to LOW
    DESCRIPTION: The test case verifies banner removed for risk level Users
    PRECONDITIONS: For the following User Risk and reason code Carousal banners should NOT be displayed
    PRECONDITIONS: "3.9", "3.10", "3.15", "3.500", "4.3", "4.9", "4.10", "4.15", "4.500", "4.600", "4.601", "4.602", "4.603", "4.604", "5.3", "5.9", "5.10", "5.15", "5.501", "5.502", "5.503", "5.600", "5.601", "5.602", "5.603", "5.604"
    PRECONDITIONS: For banners ARC rules are configured in Site Core
    """
    keep_browser_open = True

    def test_001_login_as_high_risk_user_with_reason_codes_as_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Login as High risk User with reason codes as mentioned in Pre-Conditions
        EXPECTED: User logged in successfully
        """
        pass

    def test_002_verify_gaming_carousel_bannersbanners_for_which_arc_rules_are_configured_in_site_core(self):
        """
        DESCRIPTION: Verify gaming carousel banners
        DESCRIPTION: Banners for which ARC rules are configured in site core
        EXPECTED: Banners with ARC configurations in Site core should not be displayed to the use
        """
        pass

    def test_003_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User should be able to Logout
        """
        pass

    def test_004_re_login_with_low_level_arc_user(self):
        """
        DESCRIPTION: Re-login with Low level arc user
        EXPECTED: All banners including the banners with ARC configurations are displayed to the User
        """
        pass
