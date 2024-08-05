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
class Test_C44870135_Verify_user_can_withdraw_money(Common):
    """
    TR_ID: C44870135
    NAME: Verify user can withdraw money
    DESCRIPTION: 
    PRECONDITIONS: User is loggen in
    PRECONDITIONS: User has registered all supported card types: Visa, Master Card, Paysafecard,Neteller,Skrill
    PRECONDITIONS: Balance of account is enough for withdraw from
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
        EXPECTED: Withdraw Funds' page is opened
        EXPECTED: Drop-down list with existing registered Payment Methods is shown
        EXPECTED: Drop-down is collapsed by default
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
        EXPECTED: Successfull message: **"Your withdrawal request has been successful. Reference: #XXXXXXX"** is shown
        EXPECTED: User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_006_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decremented on amount set on step №4
        """
        pass

    def test_007_select_all_other_payment_typespaysafecard_netellerskrill_etc_and_repeat_steps__4_6(self):
        """
        DESCRIPTION: Select all other payment types(Paysafecard ,Neteller,skrill etc) and repeat steps  №4-6
        EXPECTED: 
        """
        pass
