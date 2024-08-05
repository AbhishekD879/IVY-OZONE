import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1937473_Suggested_Amount_Tracking(Common):
    """
    TR_ID: C1937473
    NAME: Suggested Amount Tracking
    DESCRIPTION: This test case verifies tracking of Suggested Amount in GA
    DESCRIPTION: AUTOTEST for Skrill: [C2160182]
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=GA&title=Coral+Deposit+Journey
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has a valid payment account
    PRECONDITIONS: * Balance is enough for deposit from
    PRECONDITIONS: Payment Accounts:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: NOTE:
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    PRECONDITIONS: Steps
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: 
        """
        pass

    def test_002_tap_deposit_at_the_top_of_the_right_menu_or_on_the_betslip_page(self):
        """
        DESCRIPTION: Tap **Deposit** at the top of the Right menu or on the Betslip page
        EXPECTED: - **Deposit** page is opened
        EXPECTED: - **My Payments** tab is selected by default
        """
        pass

    def test_003_tap_add_paysafecard_tab_or_select_paysafecard_from_dropdown_list_on_my_payments_tab_if_successful_transaction_was_conducted_via_paysafecard_before(self):
        """
        DESCRIPTION: Tap **Add Paysafecard** tab or select Paysafecard from dropdown list on **My Payments** tab (if successful transaction was conducted via Paysafecard before)
        EXPECTED: 
        """
        pass

    def test_004_enter_valid_amount_via_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount via quick deposit buttons
        EXPECTED: - The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'suggested amount',
        EXPECTED: 'eventLabel' : '<< SELECTED AMOUNT >>'
        EXPECTED: });
        """
        pass

    def test_005_repeat_steps_3_and_4_for_the_following_payment_methods_skrill_skrill_1_tap_paypal(self):
        """
        DESCRIPTION: Repeat steps 3 and 4 for the following Payment Methods:
        DESCRIPTION: * Skrill
        DESCRIPTION: * Skrill 1-Tap
        DESCRIPTION: * PayPal
        EXPECTED: 
        """
        pass
