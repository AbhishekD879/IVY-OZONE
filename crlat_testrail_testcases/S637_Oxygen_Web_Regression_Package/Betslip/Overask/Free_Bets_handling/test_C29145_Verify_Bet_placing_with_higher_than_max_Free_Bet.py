import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29145_Verify_Bet_placing_with_higher_than_max_Free_Bet(Common):
    """
    TR_ID: C29145
    NAME: Verify Bet placing with higher than max. Free Bet
    DESCRIPTION: This test case verifies that user can use free bets after Overask was triggered and bet was confirmed by Trader
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-6575 Overask - Trader's complex actions - Bet Modification
    DESCRIPTION: BMA-9488 Overask - Handle freebets
    PRECONDITIONS: 1. User with free bets available is logged in to application
    PRECONDITIONS: How to add free bet:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Manually+Add+Freebet+Token+to+Account?preview=/36604221/36604223/HowToManuallyAddFreebetTokenToAccount.pdf
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added. Free bet dropdown is available and active.
        """
        pass

    def test_002_select_free_bet_which_is_higher_than_max_allowed(self):
        """
        DESCRIPTION: Select free bet which is higher than max allowed
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004_trigger_stake_confirmation_by_trader_and_verify_betslip_displaying(self):
        """
        DESCRIPTION: Trigger Stake confirmation by Trader and verify Betslip displaying
        EXPECTED: *   Bet is placed
        EXPECTED: *   Bet receipt is shown to user
        EXPECTED: *   Buttons displayed ' Reuse selection' and 'Done'
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        """
        pass

    def test_005_tap__donego_bettingfrom_ox_99_button(self):
        """
        DESCRIPTION: Tap ' Done'/'Go Betting'(From OX 99) button
        EXPECTED: Betslip is cleared
        EXPECTED: **From OX 99**
        EXPECTED: Betslip is cleared and closed
        """
        pass

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_select_free_bet_with_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them select free bet with stake value which will trigger Overask for the selection
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: *   Bets are placed
        EXPECTED: *   Bet receipt is shown to user
        EXPECTED: *   Buttons displayed ' Reuse selection' and 'Done'
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        """
        pass

    def test_008_tap_reuse_selectionnot_valid_step_from_ox_99(self):
        """
        DESCRIPTION: Tap 'Reuse selection'
        DESCRIPTION: (not valid step from OX 99)
        EXPECTED: All selections,bets were placed in step 8 appear in betslip
        """
        pass
