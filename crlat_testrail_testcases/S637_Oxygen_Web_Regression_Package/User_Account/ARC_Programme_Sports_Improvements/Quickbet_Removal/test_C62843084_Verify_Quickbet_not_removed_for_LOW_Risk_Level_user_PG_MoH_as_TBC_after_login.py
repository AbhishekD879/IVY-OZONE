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
class Test_C62843084_Verify_Quickbet_not_removed_for_LOW_Risk_Level_user_PG_MoH_as_TBC_after_login(Common):
    """
    TR_ID: C62843084
    NAME: Verify Quickbet not removed for LOW Risk Level user-PG-MoH as TBC after login
    DESCRIPTION: The test case verifies the quickbet feature get removed for risk level users
    PRECONDITIONS: Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: Configure in CMS like input Model as Problem Gamblers and Risk Level as LOW AND MoH as TBC
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_application_as_low_risk_user_gt_add_one_selection(self):
        """
        DESCRIPTION: Login into Oxygen Application as LOW risk User-&gt; add one selection
        EXPECTED: User logged in & added bet successfully to quickbet
        """
        pass

    def test_002_verify_quick_bet_feature_is_enable(self):
        """
        DESCRIPTION: Verify quick bet feature is enable
        EXPECTED: Quick bet feature should be enabled
        """
        pass

    def test_003_verify_quik_bet_option_is_enables_in_betting_settings(self):
        """
        DESCRIPTION: Verify Quik bet option is enables in betting settings
        EXPECTED: Quick bet should be in enabled state and hidden
        """
        pass

    def test_004_logout_from_the_oxygen_application(self):
        """
        DESCRIPTION: logout from the Oxygen application
        EXPECTED: Should be logged out
        """
        pass

    def test_005_access_the_oxygen_application(self):
        """
        DESCRIPTION: Access the Oxygen Application
        EXPECTED: Should be able to access
        """
        pass

    def test_006_add_one_selection_to_quickbet(self):
        """
        DESCRIPTION: Add One selection to QuickBet
        EXPECTED: Added to Quickbet
        """
        pass

    def test_007_enter_stake_value(self):
        """
        DESCRIPTION: Enter Stake value
        EXPECTED: User entered Stake
        """
        pass

    def test_008_now_try_to_login_from_quickbet_screen_as_low_risk_user_and_check_that_user_redirected_to_betslip_with_pre_filled_stake_entered(self):
        """
        DESCRIPTION: Now, Try to Login from Quickbet screen as LOW risk User and check that user redirected to Betslip with pre filled stake entered
        EXPECTED: User logged in and User stays in Quick Bet Screen
        EXPECTED: [NOT redirected to betslip with presilled stake values]
        """
        pass
