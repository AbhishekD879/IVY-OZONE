import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C28299_Verify_Successful_Withdrawing_via_Credit_Debit_Cards(Common):
    """
    TR_ID: C28299
    NAME: Verify Successful Withdrawing via Credit/Debit Cards
    DESCRIPTION: This test case verifies Successful Withdraw functionality via credit/debit cards.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-817 (Customer can withdraw funds from their Coral account)
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered all supported card types: **Visa, Visa Electron, Master Card, Maestro**
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_select_visa_card_from_drop_down_list(self):
        """
        DESCRIPTION: Select '**Visa**' card from drop-down list
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Successfull message: **"Your withdrawal request has been successful. Reference: #XXXXXXX"** is shown
        EXPECTED: *   User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_006_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decremented on amount set on step №4
        """
        pass

    def test_007_select_visa_electron_card_from_drop_down_list(self):
        """
        DESCRIPTION: Select '**Visa Electron**' card from drop-down list
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps №4-6
        EXPECTED: 
        """
        pass

    def test_009_select_master_card_card_from_drop_down_list(self):
        """
        DESCRIPTION: Select '**Master Card**' card from drop-down list
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps №4-6
        EXPECTED: 
        """
        pass

    def test_011_select_maestro_card_from_drop_down_list(self):
        """
        DESCRIPTION: Select '**Maestro**' card from drop-down list
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps №4-6
        EXPECTED: 
        """
        pass
