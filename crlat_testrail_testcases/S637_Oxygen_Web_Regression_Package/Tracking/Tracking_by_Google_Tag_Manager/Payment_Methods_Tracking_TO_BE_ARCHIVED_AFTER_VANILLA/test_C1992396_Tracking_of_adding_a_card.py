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
class Test_C1992396_Tracking_of_adding_a_card(Common):
    """
    TR_ID: C1992396
    NAME: Tracking of adding a card
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of adding a card
    PRECONDITIONS: - The test case should be run on Mobile, Tablet and Wrappers
    PRECONDITIONS: - Browser console should be opened
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - The following credit cards should be added: Mastercard, Visa, Visa Electron, Maestro
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_right_menu_icon__deposit(self):
        """
        DESCRIPTION: Tap Right menu icon > Deposit
        EXPECTED: - Deposit page is opened
        EXPECTED: - My Payments tab is selected by default
        """
        pass

    def test_003_tap_add_debitcredit_cards_tab(self):
        """
        DESCRIPTION: Tap 'Add Debit/Credit Cards' tab
        EXPECTED: - 'Add Debit/Credit Cards' tab is opened
        EXPECTED: - SafeCharge add card form is shown with filled in 'Cardholder Name' field
        """
        pass

    def test_004_fill_in_all_required_fields_and_tap_continue_button(self):
        """
        DESCRIPTION: Fill in all required fields and tap 'Continue' button
        EXPECTED: - 'My Payments' tab is opened
        EXPECTED: - Success message 'Your card was added successfully.' is displayed
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add card',
        EXPECTED: 'eventLabel' : 'success'
        EXPECTED: });
        """
        pass

    def test_006_go_back_to_add_debitcredit_cards_tab(self):
        """
        DESCRIPTION: Go back to 'Add Debit/Credit Cards' tab
        EXPECTED: - 'Add Debit/Credit Cards' tab is opened
        EXPECTED: - SafeCharge add card form is shown with filled in 'Cardholder Name' field
        """
        pass

    def test_007_trigger_a_situation_where_adding_a_credit_card_failstry_to_add_non_supported_card_type_eg_american_express_credit_car(self):
        """
        DESCRIPTION: Trigger a situation where adding a credit card fails
        DESCRIPTION: >>Try to add non-supported card type (e.g. American Express Credit Car)
        EXPECTED: Message is shown on front end
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add card',
        EXPECTED: 'eventLabel' : 'failure'
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        EXPECTED: });
        """
        pass
