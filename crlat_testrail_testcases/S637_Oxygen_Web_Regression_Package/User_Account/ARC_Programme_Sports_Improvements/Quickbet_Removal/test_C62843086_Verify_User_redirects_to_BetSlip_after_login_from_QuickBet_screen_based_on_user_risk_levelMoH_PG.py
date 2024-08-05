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
class Test_C62843086_Verify_User_redirects_to_BetSlip_after_login_from_QuickBet_screen_based_on_user_risk_levelMoH_PG(Common):
    """
    TR_ID: C62843086
    NAME: Verify User redirects to BetSlip after login from QuickBet screen based on user risk level,MoH_PG
    DESCRIPTION: The test case verifies the user is redirected to betslip from quickbet screen for risk level users
    PRECONDITIONS: Pre-requisite
    PRECONDITIONS: ---------------------------------
    PRECONDITIONS: Medium : Configure in CMS like input Model as Problem Gamblers and Risk Level as MEDIUM & MoH as TBC
    PRECONDITIONS: High :
    PRECONDITIONS: Configure in CMS like input Model as Problem Gamblers and Risk Level as HIGH &  MoH as TBC
    PRECONDITIONS: V.High
    PRECONDITIONS: Configure in CMS like input Model as Problem Gamblers and Risk Level as V.HIGH & MoH as TBC
    """
    keep_browser_open = True

    def test_001_access_the_oxygen_application(self):
        """
        DESCRIPTION: Access the Oxygen application
        EXPECTED: Should be able to access
        """
        pass

    def test_002_add_one_selection_to_quickbet(self):
        """
        DESCRIPTION: Add One selection to QuickBet
        EXPECTED: Added to Quickbet
        """
        pass

    def test_003_enter_stake_value_where_user_has_sufficient_balance(self):
        """
        DESCRIPTION: Enter Stake value [where user has sufficient balance]
        EXPECTED: User entered Stake
        """
        pass

    def test_004_now_try_to_login_from_quickbet_screen_as_medium_risk_user_and_check_that_user_redirected_to_betslip_with_pre_filled_stake_entered(self):
        """
        DESCRIPTION: Now, Try to Login from Quickbet screen as Medium risk user and check that user redirected to Betslip with pre filled stake entered
        EXPECTED: User logged in and redirected to betslip with presilled stake values
        """
        pass

    def test_005_verify_selection_details_stake_and_place_bet_button_is_displayed_in_betslip(self):
        """
        DESCRIPTION: Verify Selection details ,stake and Place Bet button is displayed in betslip
        EXPECTED: User should get Selection Details,Stake ,Place Bet button
        """
        pass

    def test_006_place_bet_from_betslip(self):
        """
        DESCRIPTION: Place bet from Betslip
        EXPECTED: bet should be placed succesfully
        """
        pass

    def test_007_logout_from_the_oxygen_application_and(self):
        """
        DESCRIPTION: Logout from the Oxygen application and
        EXPECTED: User should be logged out from Application
        """
        pass

    def test_008_check_for_high_and_very_high_risk_levels(self):
        """
        DESCRIPTION: Check for HIGH and VERY HIGH risk levels
        EXPECTED: Should be Same behaviour for High and Very High risk level users
        """
        pass
