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
class Test_C2745405_Verify_tracking_of_successful_withdrawal(Common):
    """
    TR_ID: C2745405
    NAME: Verify tracking of successful withdrawal
    DESCRIPTION: This test case verifies tracking of successful withdrawal in GA
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has valid payment accounts:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: 3. Balance is enough for withdrawal (user has deposited from all added payment methods)
    PRECONDITIONS: 4. My Account > 'Withdraw Funds' page is opened
    PRECONDITIONS: NOTE:
    PRECONDITIONS: in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown Steps
    """
    keep_browser_open = True

    def test_001_enter_valid_amount_manually_or_via_quick_deposit_buttons__tap_withdraw_funds(self):
        """
        DESCRIPTION: Enter valid amount manually or via quick deposit buttons > Tap 'Withdraw Funds'
        EXPECTED: Withdrawal has been successful
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console dataLayer, tap 'Enter' and check the response
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'withdrawal',
        EXPECTED: 'eventAction' : 'attempt',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'withdrawalAmount' : <<WITHDRAWAL AMOUNT>> e.g. 30 or 30.75
        EXPECTED: });
        """
        pass

    def test_003_repeat_steps_1_3_for_the_following_payment_methods__credit_cards_eg_visa_visa_electron_master_card_maestro__neteller__skrill__paypal(self):
        """
        DESCRIPTION: Repeat steps 1-3 for the following Payment Methods:
        DESCRIPTION: - Credit cards (e.g. Visa, Visa Electron, Master Card, Maestro)
        DESCRIPTION: - Neteller
        DESCRIPTION: - Skrill
        DESCRIPTION: - PayPal
        EXPECTED: 
        """
        pass
