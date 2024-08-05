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
class Test_C852698_Tracking_of_successful_deposit_via_Quick_Deposit(Common):
    """
    TR_ID: C852698
    NAME: Tracking of successful deposit via Quick Deposit
    DESCRIPTION: This test case verifies tracking of successful deposit via Quick Deposit within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: 4. User has the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: 5. In order to check response open Dev Tools -> select Network -> WS -> Frames section
    PRECONDITIONS: 6. Browser console should be opened
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=108597065
    PRECONDITIONS: AUTOTEST: [C1293554]
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
        EXPECTED: * Success message is displayed
        EXPECTED: * User`s balance is increased
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': <<id number>>,
        EXPECTED: 'revenue': '1'
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<< DEPOSIT NAME >>',
        EXPECTED: 'id': '<< DEPOSIT NUMBER >>',
        EXPECTED: 'price': '1',
        EXPECTED: 'category': 'credit card',
        EXPECTED: 'quantity': 1
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: },
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/deposit/success',
        EXPECTED: 'location' : 'quickbet'
        EXPECTED: });
        """
        pass

    def test_008_verify_actionfiendid_parameter(self):
        """
        DESCRIPTION: Verify **actionFiend.id** parameter
        EXPECTED: **actionFiend.id** parameter corresponds to **data.payments.transaction.[i].code** value from 33015 response in WS
        EXPECTED: where [i] - number of transaction
        """
        pass

    def test_009_verify_productname_parameter(self):
        """
        DESCRIPTION: Verify **product.name** parameter
        EXPECTED: **product.name** parameter consists of two part: **'Desposit'** + **data.payments.statictic.deposits.totalDepositCount** value from 35210 response in WS
        EXPECTED: e.g. 'Deposit 142'
        """
        pass

    def test_010_verify_productid_parameter(self):
        """
        DESCRIPTION: Verify **product.id** parameter
        EXPECTED: **product.id** parameter correspods to **data.payments.statictic.deposits.totalDepositCount** value from 35210 response in WS
        """
        pass

    def test_011_select_visa_electron_card_and_repeat_steps_6_10(self):
        """
        DESCRIPTION: Select **Visa Electron** card and repeat steps #6-10
        EXPECTED: 
        """
        pass

    def test_012_select_master_card_card_and_repeat_steps_6_10(self):
        """
        DESCRIPTION: Select **Master Card** card and repeat steps #6-10
        EXPECTED: 
        """
        pass

    def test_013_select_maestro_card_and_repeat_steps_6_10(self):
        """
        DESCRIPTION: Select **Maestro** card and repeat steps #6-10
        EXPECTED: 
        """
        pass
