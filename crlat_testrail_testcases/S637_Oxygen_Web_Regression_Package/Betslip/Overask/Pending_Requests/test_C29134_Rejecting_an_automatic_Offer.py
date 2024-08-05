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
class Test_C29134_Rejecting_an_automatic_Offer(Common):
    """
    TR_ID: C29134
    NAME: Rejecting an automatic Offer
    DESCRIPTION: This test case verifies rejecting an automatic Overask offer
    DESCRIPTION: AUTOTEST [C528030]
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    PRECONDITIONS: NOTE: System always automatically declined bet during testing
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_button_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004_wait_till_the_request_expires_without_traders_offer_for_max_bet(self):
        """
        DESCRIPTION: Wait till the Request expires without Trader's Offer for Max Bet
        EXPECTED: - A maximum automatic bet offer is shown to the user
        EXPECTED: - Check box next to selection is unchecked
        EXPECTED: - 'Accept & Bet' (inactive) and 'Cancel' buttons are present
        EXPECTED: **From OX 99**
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        EXPECTED: ![](index.php?/attachments/get/33805) ![](index.php?/attachments/get/33804)
        """
        pass

    def test_005_click__tap_continue_go_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/ 'Go betting' (From OX 99) button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        pass

    def test_006_add_few_selections_and_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections and for one of them enter stake value which will trigger overask for the selection
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps 3-6
        EXPECTED: *   No bets are placed even if these Selections did not trigger the Overask
        EXPECTED: *   All selections stay in Betslip allowing Customer to modify and resubmit it
        EXPECTED: **From OX 99**
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        EXPECTED: ![](index.php?/attachments/get/33805) ![](index.php?/attachments/get/33804)
        """
        pass
