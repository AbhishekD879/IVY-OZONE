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
class Test_C852699_Tracking_of_unsuccessful_deposit_via_Quick_Deposit(Common):
    """
    TR_ID: C852699
    NAME: Tracking of unsuccessful deposit via Quick Deposit
    DESCRIPTION: This test case verifies tracking of unsuccessful deposit via Quick Deposit within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: 4. User has the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: 5. In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: 6. Browser console should be opened
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=108597065
    PRECONDITIONS: AUTOTEST: [C1294734]
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Funds needed for bet "<currency symbol>XX.XX' error message is displayed below 'QUICK BET' header
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - entered stake value
        """
        pass

    def test_004_tap_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A QUICK DEPOSIT' button
        EXPECTED: 'QUICK DEPOSIT' section is displayed
        """
        pass

    def test_005_select_visa_card(self):
        """
        DESCRIPTION: Select **Visa** card
        EXPECTED: 
        """
        pass

    def test_006_enter_valid_cvv_amount_and_tap_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Enter valid CVV, amount and tap 'MAKE A QUICK DEPOSIT' button
        EXPECTED: * Error message is displayed
        EXPECTED: * User`s balance is not increased
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'submission',
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>',
        EXPECTED: 'paymentMethod' : 'credit card',
        EXPECTED: 'location' : 'quickbet'
        EXPECTED: });
        """
        pass

    def test_008_verify_errormessage_parameter(self):
        """
        DESCRIPTION: Verify **'errorMessage'** parameter
        EXPECTED: * **'errorMessage'** parameter to the message that user sees
        EXPECTED: * Error message is received in **data.error.errorMessage** value from 33014 response in WS
        """
        pass

    def test_009_verify_errorcode_parameter(self):
        """
        DESCRIPTION: Verify **'errorCode'** parameter
        EXPECTED: * **'errorCode'** parameter corresponds to **data.error.errorCode** value from 33014 response in WS
        EXPECTED: *  **'errorCode'** parameter corresponds to **data.errorCode** value 33014 response in WS if **data.error.errorCode** parameter is missing
        """
        pass

    def test_010_select_visa_electron_card_and_repeat_steps_6_9(self):
        """
        DESCRIPTION: Select **Visa Electron** card and repeat steps #6-9
        EXPECTED: 
        """
        pass

    def test_011_select_master_card_card_and_repeat_steps_6_9(self):
        """
        DESCRIPTION: Select **Master Card** card and repeat steps #6-9
        EXPECTED: 
        """
        pass

    def test_012_select_maestro_card_and_repeat_steps_6_9(self):
        """
        DESCRIPTION: Select **Maestro** card and repeat steps #6-9
        EXPECTED: 
        """
        pass
