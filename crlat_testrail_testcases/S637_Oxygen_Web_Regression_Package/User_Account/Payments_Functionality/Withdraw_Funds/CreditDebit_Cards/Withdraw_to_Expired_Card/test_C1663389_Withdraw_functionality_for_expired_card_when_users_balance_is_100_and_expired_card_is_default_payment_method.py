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
class Test_C1663389_Withdraw_functionality_for_expired_card_when_users_balance_is_100_and_expired_card_is_default_payment_method(Common):
    """
    TR_ID: C1663389
    NAME: Withdraw functionality for expired card when user's balance is > 100 and expired card is default payment method
    DESCRIPTION: This test case verifies Withdraw functionality for expired card when user's balance is > 100 and expired card is default payment method
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a card that expired
    PRECONDITIONS: User balance is > 100 and expired card is a default payment method
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon__withdraw(self):
        """
        DESCRIPTION: Tap Right menu icon > Withdraw
        EXPECTED: 'Withdraw' page is opened
        EXPECTED: Only expired card is available in payments method dropdown.
        EXPECTED: Wuthdraw button is disabled.
        EXPECTED: "Sorry, but your credit/debit card is expired. Please contact the helpdesk to resolve the issue."
        EXPECTED: 'Helpdesk' is hyperlinked.
        """
        pass

    def test_002_click_helpdesk_link(self):
        """
        DESCRIPTION: Click Helpdesk link
        EXPECTED: User is redirected to https://help.coral.co.uk/s
        """
        pass
