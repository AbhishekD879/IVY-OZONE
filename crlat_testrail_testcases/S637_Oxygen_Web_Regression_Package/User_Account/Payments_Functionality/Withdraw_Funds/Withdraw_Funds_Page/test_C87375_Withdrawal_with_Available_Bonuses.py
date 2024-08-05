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
class Test_C87375_Withdrawal_with_Available_Bonuses(Common):
    """
    TR_ID: C87375
    NAME: Withdrawal with Available Bonuses
    DESCRIPTION: This test case verifies user's attempt to withdraw with available bonuses, in particular handling PAYMENTS-1012 code
    DESCRIPTION: Cannot automate as we need to add casino bonuses in IMS which is manual step
    PRECONDITIONS: * User is logged in and has available bonuses
    PRECONDITIONS: * Web console with Network -> WS  tab is opened
    PRECONDITIONS: To trigger bonuses follow the instructions: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+trigger+casino+bonuses but select 'Pre-wager' value in the 'Bonus type' field and 'AWOL bonus' value in the 'Bonus Template' field
    """
    keep_browser_open = True

    def test_001_navigate_to_withdraw_page(self):
        """
        DESCRIPTION: Navigate to Withdraw page
        EXPECTED: 
        """
        pass

    def test_002_enter_amount_of_money_not_more_than_user_balance(self):
        """
        DESCRIPTION: Enter amount of money (not more than user balance)
        EXPECTED: 
        """
        pass

    def test_003_click_withdraw_funds_button(self):
        """
        DESCRIPTION: Click 'Withdraw Funds' button
        EXPECTED: Pop up message appears
        """
        pass

    def test_004_observe_websockets_frames(self):
        """
        DESCRIPTION: Observe Websocket's frames
        EXPECTED: * Withdrawal Request (33017) is sent
        EXPECTED: * Withdrawal Error (33019) with PAYMENTS-1012 code is received
        EXPECTED: Note: In case Withdrawal Response (33018) is received withdrawal is successful
        """
        pass

    def test_005_veriify_pop_up_message(self):
        """
        DESCRIPTION: Veriify pop up message
        EXPECTED: Pop up message consists of the following:
        EXPECTED: *  TITLE: empty
        EXPECTED: *  BODY: 'error' -> 'message' parameter from Deposit Error (33014) response'
        EXPECTED: *  BUTTONS: 'Accept' and 'Decline'
        """
        pass

    def test_006_click_decline_button(self):
        """
        DESCRIPTION: Click 'Decline' button
        EXPECTED: * Pop up message is closed
        EXPECTED: * Withdrawal Request (33017) is NOT resent
        EXPECTED: * Data, entered in step #2, is not cleared
        EXPECTED: * Withdrawal is not completed
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_008_click_accept_button(self):
        """
        DESCRIPTION: Click 'Accept' button
        EXPECTED: * Withdrawal Request (33017) is resent with parameter loseBonus=true
        EXPECTED: * Withdrawal is successful
        """
        pass
