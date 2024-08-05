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
class Test_C832557_Verify_Callback_to_Casino_app_after_happy_path_of_depositing_via_credit_debit_card(Common):
    """
    TR_ID: C832557
    NAME: Verify Callback to Casino app after happy path of depositing via credit/debit card
    DESCRIPTION: This test case verifies the functionality of a callback to Casino app after successful completion of the BMA depositing via credit/debit card
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has registered Debit/Credit Cards from which they can deposit funds from (e.g. user: khrystyna/111111; Visa \***| \***| \***| 5081, any CV2)
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: BMA-5238
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urldepositregisteredcburlcasino_urleghttpsinvictuscoralcoukdepositregisteredcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/**#/deposit/registered?****cbURL=**<Casino_url>
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/#/deposit/registered?cbURL=http://mcasino-tst2.coral.co.uk
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   'Registered' tab is selected by default
        """
        pass

    def test_002_select_creditdebit_card(self):
        """
        DESCRIPTION: Select **Credit/Debit Card**
        EXPECTED: 
        """
        pass

    def test_003_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_004_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   Successfull message is shown
        EXPECTED: *   **User is redirected to Casino application (e.g. http://mcasino-tst2.coral.co.uk)**
        EXPECTED: *   User is logged in there automaticaly
        EXPECTED: *   User Balance is increased accordingly
        """
        pass
