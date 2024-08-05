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
class Test_C524815_Verify_tracking_of_deposit_success_failure_and_field_completions_when_user_is_redirected_from_Gaming(Common):
    """
    TR_ID: C524815
    NAME: Verify tracking of deposit success, failure, and field completions when user is redirected from Gaming
    DESCRIPTION: This test case verifies tracking of deposit success, failure, and field completions for case, when user is redirected from Gaming.
    DESCRIPTION: For reference, please see test cases:
    DESCRIPTION: * [Tracking of Successful Deposit] [1]
    DESCRIPTION: * [Tracking of Failed Deposit] [2]
    DESCRIPTION: * [Tracking of fields completion during depositing] [3]
    DESCRIPTION: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/87380
    DESCRIPTION: [2]: https://ladbrokescoral.testrail.com/index.php?/cases/view/87381
    DESCRIPTION: [3]: https://ladbrokescoral.testrail.com/index.php?/cases/view/110818
    PRECONDITIONS: * User is logged in to Oxygen application
    PRECONDITIONS: * User has the following cards: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: * User has Netteler and PayPal accounts
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet and Desktop
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: As soon as user completes deposit, he is redirected back to Gaming site. The amount of time between finishing deposit and the redirect is not enough to check dataLayer in console (redirect is made very fast). Therefore, to run this test case, dev assistance is needed.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen application and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_gaming(self):
        """
        DESCRIPTION: Navigate to Gaming
        EXPECTED: User is navigated to Gaming
        """
        pass

    def test_003_on_gaming_page_tap_balance_button(self):
        """
        DESCRIPTION: On Gaming page, tap 'Balance' button
        EXPECTED: Right menu is opened
        """
        pass

    def test_004_select_deposit_from_the_right_menu(self):
        """
        DESCRIPTION: Select 'Deposit' from the right menu
        EXPECTED: User is redirected to 'Deposit' page in Oxygen application
        """
        pass

    def test_005_select_a_card_from_the_drop_down_menu_with_payment_methods(self):
        """
        DESCRIPTION: Select a card from the drop-down menu with payment methods
        EXPECTED: Card is selected
        """
        pass

    def test_006_enter_a_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter a valid CV2 into 'CV2' field
        EXPECTED: CV2 is entered
        """
        pass

    def test_007_type_datalayer_in_console_hit_enter_key(self):
        """
        DESCRIPTION: Type 'dataLayer' in console, hit 'Enter' key
        EXPECTED: dataLayer with Objects is shown
        """
        pass

    def test_008_expand_the_last_object(self):
        """
        DESCRIPTION: Expand the last Object
        EXPECTED: The next static parameters are present:
        EXPECTED: `dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : '<<<field name>>>',
        EXPECTED: 'paymentMethod' : '<<<payment method>>>',
        EXPECTED: 'location' : '<<<location>>>' }
        EXPECTED: ); `
        EXPECTED: WHERE:
        EXPECTED: * <<<field name>>> - the name of the label of the field
        EXPECTED: * <<<payment method>>> - payment method used ('credit card' - for Visa, Visa Electron, Master Card and Maestro cards, 'paypal' - for PayPal, 'neteller' - for Neteller)
        EXPECTED: * <<<location>>> - where the customer is depositing from (in this case - 'my account')
        """
        pass

    def test_009_enter_a_valid_amount_into_enter_amount_field_and_repeat_steps_6_7(self):
        """
        DESCRIPTION: Enter a valid amount into 'Enter Amount' field and repeat steps 6-7
        EXPECTED: 
        """
        pass

    def test_010_make_a_successful_deposit_with_the_card_and_check_datalayer(self):
        """
        DESCRIPTION: Make a successful deposit with the card and check dataLayer
        EXPECTED: The next static parameters are present:
        EXPECTED: `dataLayer.push({
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField':
        EXPECTED: { 'id': '<<<id number>>>', 'revenue': '1' }
        EXPECTED: ,
        EXPECTED: 'products': [
        EXPECTED: { 'name': '<<< DEPOSIT NAME >>>', 'id': '<<< DEPOSIT NUMBER >>>', 'price': '1', 'category': '<<< PAYMENT TYPE >>>', 'quantity': 1 }
        EXPECTED: ]
        EXPECTED: }
        EXPECTED: },
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/deposit/success',
        EXPECTED: 'depositLocation' : '<<< DEPOSIT LOCATION >>>'
        EXPECTED: }) `
        EXPECTED: WHERE:
        EXPECTED: * <<<id number>>> - ID number is equal the the transaction ID passed from IMS; in WebSockets value for code in response {data: {payments: {transaction:}}
        EXPECTED: * <<< DEPOSIT NAME >>> - the deposit number passed as part of the name; in WebSockets value for totalDepositCount in response {data: {payments: {statistics: deposits:}}}
        EXPECTED: * <<< DEPOSIT NUMBER >>> - the sequential deposit number that is passed from IMS; in WebSockets value for totalDepositCount in response {data: {payments: {statistics: deposits:}}}
        """
        pass

    def test_011_repeat_steps_5_10_for_the_following_payment_methods_mastercard_visa_visa_electron_maestro_paypal_netellernote_user_has_to_navigate_from_gaming_every_time_when_changing_payment_method(self):
        """
        DESCRIPTION: Repeat steps 5-10 for the following payment methods:
        DESCRIPTION: * MasterCard
        DESCRIPTION: * Visa
        DESCRIPTION: * Visa Electron
        DESCRIPTION: * Maestro
        DESCRIPTION: * PayPal
        DESCRIPTION: * Neteller
        DESCRIPTION: **NOTE:** User has to navigate from Gaming every time when changing payment method.
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: 
        """
        pass

    def test_013_enter_data_into_all_required_fields_part_of_which_is_invalid_for_example_cv2_for_card_or_secure_id_for_neteller_and_tap_deposit_button(self):
        """
        DESCRIPTION: Enter data into all required fields, part of which is invalid (for example CV2 for card or Secure ID for Neteller) and tap 'Deposit' button
        EXPECTED: Deposit attempt was unsuccessful, error message appears
        """
        pass

    def test_014_verify_last_frame_in_websocket_section_in_network_tab_in_console(self):
        """
        DESCRIPTION: Verify last frame in websocket section in Network tab in Console
        EXPECTED: Deposit error response 33014 is received
        """
        pass

    def test_015_type_in_console_datalayer_press_enter_and_expand_needed_object_should_be_the_last_one(self):
        """
        DESCRIPTION: Type in console dataLayer, press 'Enter' and expand needed Object (should be the last one)
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: `'event': 'trackEvent'
        EXPECTED: 'eventCategory': 'deposit'
        EXPECTED: 'eventAction': ' 'submission'
        EXPECTED: 'eventLabel': 'failure'
        EXPECTED: 'errorMesage': '<error message>'
        EXPECTED: 'errorCode': '<error code>'
        EXPECTED: 'paymentMethod': 'credit card' OR 'neteller' OR 'paypal' (appropriate one)
        EXPECTED: 'location': 'my account' OR 'betslip' (appropriate one), `
        EXPECTED: WHERE:
        EXPECTED: *  <error code> is equal to the back end error code (is taken from 'error.code' attribute. If this one is absent, 'errorCode' value is sent),
        EXPECTED: * <error message> is equal to the front end error message that a customer sees, both of them are taken from error response and are sent in lower case and without underscore
        """
        pass

    def test_016_repeat_steps_13_16_for_the_following_payment_methods_mastercard_visa_visa_electron_maestro_paypal_netellernote_user_has_to_navigate_from_gaming_every_time_when_changing_payment_method(self):
        """
        DESCRIPTION: Repeat steps 13-16 for the following payment methods
        DESCRIPTION: * MasterCard
        DESCRIPTION: * Visa
        DESCRIPTION: * Visa Electron
        DESCRIPTION: * Maestro
        DESCRIPTION: * PayPal
        DESCRIPTION: * Neteller
        DESCRIPTION: **NOTE:** User has to navigate from Gaming every time when changing payment method.
        EXPECTED: 
        """
        pass
