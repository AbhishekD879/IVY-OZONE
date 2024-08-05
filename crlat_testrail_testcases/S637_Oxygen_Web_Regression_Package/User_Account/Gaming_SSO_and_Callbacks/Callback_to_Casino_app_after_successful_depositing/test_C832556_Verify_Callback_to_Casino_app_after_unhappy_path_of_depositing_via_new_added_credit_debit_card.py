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
class Test_C832556_Verify_Callback_to_Casino_app_after_unhappy_path_of_depositing_via_new_added_credit_debit_card(Common):
    """
    TR_ID: C832556
    NAME: Verify Callback to Casino app after unhappy path of depositing via new added credit/debit card
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after adding new credit/debit card and unhappy path depositing via this card
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has no registered cards
    PRECONDITIONS: In order to get number of credit card the following links can be used:
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: Jira ticket: BMA-5854
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urldepositregisteredcburlcasino_urleghttpsinvictuscoralcoukdepositregisteredcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/deposit/registered?****cbURL=**<Casino_url>
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/#/deposit/registered?cbURL=http://mcasino-tst2.coral.co.uk
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   'Registered' tab is selected by default
        EXPECTED: *   Message 'Please visit the *Debit/Credit Cards* to deposit using your card.' is shown
        """
        pass

    def test_002_tap_debitcredit_cards_hyperlink(self):
        """
        DESCRIPTION: Tap 'Debit/Credit Cards' hyperlink
        EXPECTED: *   'Debit/Credit Cards' tab is opened
        EXPECTED: *   SafeCharge add card form is shown with filled in 'Cardholder Name' field
        """
        pass

    def test_003_enter_invalid_card_number_expiration_date_and_tap_continue_button(self):
        """
        DESCRIPTION: Enter invalid Card Number, Expiration date and tap 'Continue' button
        EXPECTED: *   Error message is shown
        EXPECTED: *   **User stays on the 'Debit/Credit Cards' tab on BMA app**
        """
        pass

    def test_004_enter_validcard_number_expiration_date_and_tap_continue_button(self):
        """
        DESCRIPTION: Enter valid Card Number, Expiration date and tap 'Continue' button
        EXPECTED: *   'Registered' tab is opened
        EXPECTED: *   Success message **'Your card was added successfully.'** is displayed
        """
        pass

    def test_005_verify_unsuccessful_depositingenter_amount_than_is_higher_than_balance_on_the_users_cards_manually_or_using_quick_deposit_buttons_and_tap_deposit_button(self):
        """
        DESCRIPTION: Verify unsuccessful depositing:
        DESCRIPTION: Enter amount than is higher than balance on the user's cards manually or using quick deposit buttons and tap 'Deposit' button
        EXPECTED: *   Error message is shown
        EXPECTED: *   **User stays on the 'Registered' tab on BMA app**
        EXPECTED: *   All fields are cleared
        """
        pass

    def test_006_enter_valid_amount_manually_or_using_quick_deposit_buttons_and_tap_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons and tap 'Deposit' button
        EXPECTED: *   Successfull message is shown
        EXPECTED: *   **User is redirected to Casino application (e.g. http://mcasino-tst2.coral.co.uk)**
        EXPECTED: *   User is logged in there automaticaly
        EXPECTED: *   User Balance is increased accordingly
        """
        pass
