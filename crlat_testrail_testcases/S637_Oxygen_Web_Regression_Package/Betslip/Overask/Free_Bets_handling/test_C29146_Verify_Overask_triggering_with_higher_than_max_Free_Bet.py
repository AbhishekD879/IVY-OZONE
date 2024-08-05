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
class Test_C29146_Verify_Overask_triggering_with_higher_than_max_Free_Bet(Common):
    """
    TR_ID: C29146
    NAME: Verify Overask triggering with higher than max. Free Bet
    DESCRIPTION: This test case verifies that freebet gets unselected if it was selected before Overask was triggered
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

    def test_002_select_free_bet_with_valuewhich_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Select Free bet with value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification/(overlay from OX 99)is shown to the User
        """
        pass

    def test_004_trigger_stake_modification_by_trader_and_verify_betslip_displaying(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader and verify betslip displaying
        EXPECTED: *   Info message is displayed above 'Bet Now' button with text:'Freebet cannot be used with this bet.'
        EXPECTED: *   Stake field is cleared.
        EXPECTED: *   Free Bet value is unselected in dropdown.
        EXPECTED: *   'Bet Now' button is disabled and displayed.
        EXPECTED: **From OX 99**
        EXPECTED: 'Place bet' button
        """
        pass

    def test_005_enter_some_stake_value_less_than_max_allowed(self):
        """
        DESCRIPTION: Enter some stake value less than max allowed
        EXPECTED: Stake appears in stake box
        """
        pass

    def test_006_tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: The bet is placed as per normal process
        """
        pass

    def test_007_add_few_selections_to_the_betslipand_for_one_of_them_select_free_bet_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them select free bet value which will trigger Overask for the selection
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps 3-6
        EXPECTED: Bets can not be placed using higher than max allowed free bet value.
        """
        pass
