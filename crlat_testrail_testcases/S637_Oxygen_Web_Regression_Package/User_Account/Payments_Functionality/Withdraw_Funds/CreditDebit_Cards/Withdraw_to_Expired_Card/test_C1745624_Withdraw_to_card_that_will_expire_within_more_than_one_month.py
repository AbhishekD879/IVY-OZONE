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
class Test_C1745624_Withdraw_to_card_that_will_expire_within_more_than_one_month(Common):
    """
    TR_ID: C1745624
    NAME: Withdraw to card that will expire within more than one month
    DESCRIPTION: This test case verifies ability to withdraw to a card that will expire within more than one month.
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a card that will expire within more than one month.
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon__withdraw(self):
        """
        DESCRIPTION: Tap Right menu icon > Withdraw
        EXPECTED: 'Withdraw' page is opened
        EXPECTED: Default payment method selected in dropdown
        """
        pass

    def test_002_in_payments_dropdown_select_a_card_from_preconditions(self):
        """
        DESCRIPTION: In payments dropdown select a card from preconditions
        EXPECTED: WIihdraw button is enabled.
        EXPECTED: There is no errors for user.
        """
        pass

    def test_003_input_some_amount_into_amount_field_and_click_withdraw(self):
        """
        DESCRIPTION: Input some amount into Amount field and click withdraw
        EXPECTED: Withdrawal is successful.
        EXPECTED: User balance reduced by amount entered in step 3.
        """
        pass
