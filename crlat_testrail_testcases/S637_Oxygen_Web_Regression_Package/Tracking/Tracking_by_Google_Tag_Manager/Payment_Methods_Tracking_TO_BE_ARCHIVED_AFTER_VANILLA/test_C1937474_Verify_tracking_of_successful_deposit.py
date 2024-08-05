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
class Test_C1937474_Verify_tracking_of_successful_deposit(Common):
    """
    TR_ID: C1937474
    NAME: Verify tracking of successful deposit
    DESCRIPTION: This test case verifies tracking of Deposit Success in GA
    DESCRIPTION: AUTOTEST for Skrill: [C2160382]
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=GA&title=Coral+Deposit+Journey
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has valid payment accounts:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Test+Accounts+for+Payments+Functionality+Testing
    PRECONDITIONS: NOTE:
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_deposit_valid_amount_from__my_account_deposit_page__my_payments_tabpayment_eg_add_debitcredit_cards_tab__quick_bet_quick_deposit__only_by_credit_cards__betslip_quick_deposit___only_by_credit_cards(self):
        """
        DESCRIPTION: Deposit valid amount from:
        DESCRIPTION: - My Account >'Deposit' page > 'My Payments' tab/{Payment e.g. Add Debit/Credit Cards} tab
        DESCRIPTION: - Quick Bet (Quick Deposit) > only by credit cards
        DESCRIPTION: - Betslip (Quick Deposit) >  only by credit cards
        EXPECTED: Deposit has been successful
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **dataLayer**, tap 'Enter' and check the response
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': '<<DEPOSIT TYPE>>',
        EXPECTED: 'eventAction': 'attempt',
        EXPECTED: 'eventLabel': 'success',
        EXPECTED: 'depositValue': <<DEPOSIT VALUE>>,
        EXPECTED: 'depositNumber': <<DEPOSIT NUMBER>>,
        EXPECTED: 'currencyCode': '<<CURRENCY CODE>>',
        EXPECTED: 'paymentMethod': '<<PAYMENT METHOD>>',
        EXPECTED: 'depositID': '<<DEPOSIT ID>>',
        EXPECTED: 'location' : '<<LOCATION>>'
        EXPECTED: });
        """
        pass

    def test_003_verify_deposit_type_parameter(self):
        """
        DESCRIPTION: Verify <<<DEPOSIT TYPE>>> parameter
        EXPECTED: Deposit type depends on where deposit is made from:
        EXPECTED: * deposit (My Account > My Payments or {Payment e.g. Add Debit/Credit Cards} tab)
        EXPECTED: * quick deposit (Betslip/Quick Bet)
        """
        pass

    def test_004_verify__deposit_number__parameter(self):
        """
        DESCRIPTION: Verify <<< DEPOSIT NUMBER >>> parameter
        EXPECTED: Deposit number should equal the sequential deposit number that is passed from IMS e.g <totaldepositcount>
        EXPECTED: In WebSockets value for totalDepositCount in response {data: {payments: {statistics: deposits:}}}
        EXPECTED: (e.g. 3:{"data":{"payments":{"statistics":{"deposits":{"totalDepositCount":"40",}
        """
        pass

    def test_005_verify__currency_code__parameter(self):
        """
        DESCRIPTION: Verify <<< CURRENCY CODE >>> parameter
        EXPECTED: Depends on the user's account currency:
        EXPECTED: * GBD
        EXPECTED: * EUR
        EXPECTED: * USD
        EXPECTED: * SEK
        """
        pass

    def test_006_verify__payment_method__parameter(self):
        """
        DESCRIPTION: Verify <<< PAYMENT METHOD >>> parameter
        EXPECTED: Payment method is equal the payment method used.
        EXPECTED: In WebSockets value for code in response {data: {payments: {method:}}}
        EXPECTED: * Credit Card (Master Card,Visa, Visa Electron, Maestro)
        EXPECTED: * Neteller
        EXPECTED: * Skrill
        EXPECTED: * Skrill 1-Tap
        EXPECTED: * PayPal
        EXPECTED: * Paysafecard
        """
        pass

    def test_007_verify__deposit_id__parameter(self):
        """
        DESCRIPTION: Verify <<< DEPOSIT ID >>> parameter
        EXPECTED: ID number is equal the the transaction ID passed from IMS (reference code for the payment).
        EXPECTED: In WebSockets value for code in response {data: {payments: {transaction:}}
        EXPECTED: e.g.{"data":{"payments":{"transaction":[{"amount":10,"status":"approved","message":"Your credit card deposit has been approved and will be charged as CoralWebTest. Thank you and good luck!","code":"433864"}]}},"ID":33015}
        """
        pass

    def test_008_verify__deposit_location__parameter(self):
        """
        DESCRIPTION: Verify <<< DEPOSIT LOCATION >>> parameter
        EXPECTED: Deposit type depends on where deposit is made from:
        EXPECTED: * my account (My Account > My Payments or {Payment e.g. Add Debit/Credit Cards} tab)
        EXPECTED: * betslip (Quick Deposit)
        EXPECTED: * quick bet (Quick Deposit)
        """
        pass

    def test_009_repeat_steps_1_8_with_the_following_payment_methods__different_currency__credit_cards_eg_visa_visa_electron_master_card_maestro__neteller__skrill__skrill_1_tap__paypal__paysafecard(self):
        """
        DESCRIPTION: Repeat steps 1-8 with the following Payment Methods & different currency:
        DESCRIPTION: - Credit cards (e.g. Visa, Visa Electron, Master Card, Maestro)
        DESCRIPTION: - Neteller
        DESCRIPTION: - Skrill
        DESCRIPTION: - Skrill 1-Tap
        DESCRIPTION: - PayPal
        DESCRIPTION: - Paysafecard
        EXPECTED: 
        """
        pass
