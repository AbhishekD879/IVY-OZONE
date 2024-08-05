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
class Test_C62843082_Verify_Quickbet_feature_after_risk_level_changes_from_High_to_LOW_PG_MoH_as_TBC(Common):
    """
    TR_ID: C62843082
    NAME: Verify Quickbet feature after risk level changes from High to LOW-PG-MoH as TBC
    DESCRIPTION: The test case verifies the quickbet feature get removed for risk level users
    PRECONDITIONS: Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: Configure in CMS like input Model as Problem Gamblers and Risk Level as High AND MoH as TBC
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_application_as_high_risk_user__add_one_selection(self):
        """
        DESCRIPTION: Login into Oxygen Application as HIGH risk User-> add one selection
        EXPECTED: User logged in successfully
        """
        pass

    def test_002_verify_quick_bet_feature_removed_or_not(self):
        """
        DESCRIPTION: Verify quick bet feature removed or not
        EXPECTED: Quick bet feature should be removed
        """
        pass

    def test_003_verify_quik_bet_option_is_disabled_and_hidden_in_betting_settings(self):
        """
        DESCRIPTION: Verify Quik bet option is disabled and hidden in betting settings
        EXPECTED: Quick bet should be in disabled state and hidden
        """
        pass

    def test_004_login_into_cms_and_configure__input_model_as_problem_gamblers_and_risk_level_as_low_and_moh_as_tbc(self):
        """
        DESCRIPTION: Login into CMS and Configure  input Model as Problem Gamblers and Risk Level as LOW AND MoH as TBC
        EXPECTED: Configuration done
        """
        pass

    def test_005_logout_from_the_oxygen_application(self):
        """
        DESCRIPTION: logout from the Oxygen application
        EXPECTED: Should be logged out
        """
        pass

    def test_006_login_into_oxygen_application_and_add_one_selection_to_quick_bet(self):
        """
        DESCRIPTION: Login into Oxygen Application and add one selection to quick bet
        EXPECTED: User logged in & added bet successfully to quickbet
        """
        pass
