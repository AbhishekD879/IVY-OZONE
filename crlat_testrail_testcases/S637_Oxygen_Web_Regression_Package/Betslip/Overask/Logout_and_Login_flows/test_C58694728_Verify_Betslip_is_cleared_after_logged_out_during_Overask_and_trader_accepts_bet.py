import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C58694728_Verify_Betslip_is_cleared_after_logged_out_during_Overask_and_trader_accepts_bet(Common):
    """
    TR_ID: C58694728
    NAME: Verify Betslip is cleared after logged out during Overask and trader accepts bet
    DESCRIPTION: This test case verifies that Betslip is cleared after tapping logging out during OA and accepted bet is shown in My Bets and balance is updated appropriately
    PRECONDITIONS: Overask is enabled for User1 and for event which will be added to Betslip (see doc: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: Login with User1 (without 'Remember Me' option) and add selection available for Overask to Betslip
    PRECONDITIONS: Add Stake bigger than MaxAllowed
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: OX.overaskPlaceBetsData
    PRECONDITIONS: OX.overaskIsInProgress
    PRECONDITIONS: OX.overaskUsername
    PRECONDITIONS: ![](index.php?/attachments/get/106948247)
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - OA bet trigger is sent to TI (Bet>BI Request)
        """
        pass

    def test_002_trigger_log_out_from_appon_desktop_tap_logout_button_in_account_menuon_web_mobile_refresh_page_or_close_and_reopen_tab_and_then_taplogout_button_in_the_account_menuon_wrappers_kill_and_reopen_the_app(self):
        """
        DESCRIPTION: Trigger log out from app:
        DESCRIPTION: **On Desktop:** Tap 'Logout' button in account menu
        DESCRIPTION: **On Web mobile:** Refresh page or close and reopen tab and then Tap'Logout' button in the account menu
        DESCRIPTION: **On wrappers:** Kill and reopen the app
        EXPECTED: - User is logged out
        EXPECTED: - Homepage is shown (for mobile web and wrappers)
        """
        pass

    def test_003_in_ti_accept_bet_betbi_request(self):
        """
        DESCRIPTION: In TI ACCEPT bet (Bet>BI Request)
        EXPECTED: 
        """
        pass

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: Selection added in preconditions is NOT shown in Betslip
        """
        pass

    def test_005_check_local_storage(self):
        """
        DESCRIPTION: Check Local Storage:
        EXPECTED: - OX.overaskPlaceBetsData, OX.overaskIsInProgress, OX.overaskUsername are cleared
        EXPECTED: - OX.BetSelections is empty
        """
        pass

    def test_006_tap_login_buttonlogin_with_user1_from_preconditions(self):
        """
        DESCRIPTION: Tap 'Login' button
        DESCRIPTION: Login with user1 from preconditions
        EXPECTED: - User is logged in
        EXPECTED: - Selection added in preconditions is NOT shown in Betslip
        EXPECTED: - User balance is updated according to the Stake from preconditions
        """
        pass

    def test_007_go_to_my_bets(self):
        """
        DESCRIPTION: Go to My Bets
        EXPECTED: Bet which was accepted by trader is shown in My Bets
        """
        pass
