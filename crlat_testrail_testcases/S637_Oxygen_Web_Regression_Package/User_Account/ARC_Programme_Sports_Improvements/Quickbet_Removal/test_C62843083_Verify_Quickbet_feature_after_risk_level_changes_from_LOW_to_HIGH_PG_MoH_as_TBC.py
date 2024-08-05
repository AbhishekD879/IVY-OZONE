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
class Test_C62843083_Verify_Quickbet_feature_after_risk_level_changes_from_LOW_to_HIGH_PG_MoH_as_TBC(Common):
    """
    TR_ID: C62843083
    NAME: Verify Quickbet feature after risk level changes from LOW to HIGH -PG-MoH as TBC
    DESCRIPTION: The test case verifies the quickbet feature get removed for risk level users
    PRECONDITIONS: Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: Configure in CMS like input Model as Problem Gamblers and Risk Level as LOW AND MoH as TBC
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_application_as_low_risk_user__add_one_selection(self):
        """
        DESCRIPTION: Login into Oxygen Application as LOW risk User-> add one selection
        EXPECTED: User logged in & added bet successfully to quickbet
        """
        pass

    def test_002_verify_quick_bet_feature_present_and_selection_is_added_to_quickbet(self):
        """
        DESCRIPTION: Verify quick bet feature present and selection is added to Quickbet
        EXPECTED: Quick bet feature should be enable
        """
        pass

    def test_003_login_into_cms_and_configure__input_model_as_problem_gamblers_and_risk_level_as_high_and_moh_as_tbc(self):
        """
        DESCRIPTION: Login into CMS and Configure  input Model as Problem Gamblers and Risk Level as HIGH AND MoH as TBC
        EXPECTED: Configuration done
        """
        pass

    def test_004_logout_from_the_oxygen_application(self):
        """
        DESCRIPTION: logout from the Oxygen application
        EXPECTED: Should be logged out
        """
        pass

    def test_005_login_into_oxygen_application(self):
        """
        DESCRIPTION: Login into Oxygen Application
        EXPECTED: User logged in successfully
        """
        pass

    def test_006_verify_quick_bet_feature_removed_or_not(self):
        """
        DESCRIPTION: Verify quick bet feature removed or not
        EXPECTED: Quick bet feature should be removed
        """
        pass

    def test_007_verify_quik_bet_option_is_disabled_and_hidden_in_betting_settings(self):
        """
        DESCRIPTION: Verify Quik bet option is disabled and hidden in betting settings
        EXPECTED: Quick bet should be in disabled state and hidden
        """
        pass
