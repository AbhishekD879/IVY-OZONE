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
class Test_C2745406_Verify_tracking_of_failed_withdrawal(Common):
    """
    TR_ID: C2745406
    NAME: Verify tracking of failed withdrawal
    DESCRIPTION: This test case verifies tracking of failed withdrawal in GA
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has valid payment accounts:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: 3. Balance is enough for withdrawal (user has deposited from all added payment methods)
    PRECONDITIONS: 4. My Account > 'Withdraw Funds' page is opened
    PRECONDITIONS: NOTE:
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown Steps
    """
    keep_browser_open = True

    def test_001_trigger_the_situation_when_withdraw_is_going_to_be_failedeg_enter_amount_bigger_than_users_balance_or_enter_amount_that_exceeds_withdrawal_limit_tap_withdraw_funds(self):
        """
        DESCRIPTION: Trigger the situation when withdraw is going to be failed
        DESCRIPTION: (e.g. Enter amount bigger than user's balance OR enter amount that exceeds withdrawal limit)
        DESCRIPTION: > Tap 'Withdraw Funds'
        EXPECTED: - Withdrawal has failed
        EXPECTED: - Error message is displayed (e.g. 'The amount you wish to withdraw exceeds your current account balance.')
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
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'withdrawalAmount' : <<WITHDRAWAL AMOUNT>> e.g. 30 or 30.75,
        EXPECTED: 'errorMessage' : '<<ERROR MESSAGE>>',
        EXPECTED: 'errorCode' : '<<ERROR CODE>>'
        EXPECTED: });
        """
        pass

    def test_003_repeat_steps_1_3_for_the_following_payment_methods__credit_card__eg_visa_visa_electron_master_card_maestro__neteller__skrill__paypal(self):
        """
        DESCRIPTION: Repeat steps 1-3 for the following Payment Methods:
        DESCRIPTION: - Credit Card  (e.g. Visa, Visa Electron, Master Card, Maestro)
        DESCRIPTION: - Neteller
        DESCRIPTION: - Skrill
        DESCRIPTION: - PayPal
        EXPECTED: 
        """
        pass
