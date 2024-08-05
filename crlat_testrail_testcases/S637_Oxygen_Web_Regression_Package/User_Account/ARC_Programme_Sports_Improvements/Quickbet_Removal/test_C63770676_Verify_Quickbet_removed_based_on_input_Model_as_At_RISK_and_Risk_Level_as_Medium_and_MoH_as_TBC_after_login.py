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
class Test_C63770676_Verify_Quickbet_removed_based_on_input_Model_as_At_RISK_and_Risk_Level_as_Medium_and_MoH_as_TBC_after_login(Common):
    """
    TR_ID: C63770676
    NAME: Verify Quickbet removed based on input Model as At RISK and Risk Level as Medium and MoH as TBC after login
    DESCRIPTION: The test case verifies the quickbet feature get removed for risk level users
    PRECONDITIONS: Pre-requisite
    PRECONDITIONS: Configure in CMS like input Model as At RISK and Risk Level as Medium AND MoH as TBC
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_application_as_medium_risk_user(self):
        """
        DESCRIPTION: Login into Oxygen Application as MEDIUM risk User
        EXPECTED: User logged in successfully and
        """
        pass

    def test_002_add_one_selection_and_verify_quick_bet_feature_removed_or_not(self):
        """
        DESCRIPTION: Add one selection and Verify quick bet feature removed or not
        EXPECTED: Quick bet feature should be removed
        """
        pass

    def test_003_verify_selection_is_added_to_betslip(self):
        """
        DESCRIPTION: Verify selection is added to betslip
        EXPECTED: if Quickbet removed then It should be added to betslip
        """
        pass

    def test_004_verify_quik_bet_option_hidden_in_betting_settings(self):
        """
        DESCRIPTION: Verify Quik bet option hidden in betting settings
        EXPECTED: Quick bet should be hidden
        """
        pass

    def test_005_logout_from_the_oxygen_application(self):
        """
        DESCRIPTION: logout from the Oxygen application
        EXPECTED: Should be logged out
        """
        pass
