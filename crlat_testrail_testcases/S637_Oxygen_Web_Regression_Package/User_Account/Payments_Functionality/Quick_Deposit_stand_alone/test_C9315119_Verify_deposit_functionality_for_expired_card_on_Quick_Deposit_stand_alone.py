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
class Test_C9315119_Verify_deposit_functionality_for_expired_card_on_Quick_Deposit_stand_alone(Common):
    """
    TR_ID: C9315119
    NAME: Verify deposit functionality for expired card on 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies deposit functionality with expired card via 'Quick Deposit' stand alone
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has several cards registered on his account:
    PRECONDITIONS: - an expired card with deposits on record
    PRECONDITIONS: - an expired card without deposits on record
    PRECONDITIONS: - an unexpired card
    PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_enter_valid_values_into_cvv__deposit_amount_fields(self):
        """
        DESCRIPTION: Enter valid values into 'CVV' & 'Deposit Amount' fields
        EXPECTED: 'CVV' & 'Deposit Amount' fields are populated with entered values
        """
        pass

    def test_002_select_an_expired_card_with_deposits_on_record_in_credit_card_dropdown(self):
        """
        DESCRIPTION: Select **an expired card with deposits on record** in Credit Card Dropdown
        EXPECTED: - 'Deposit' button becomes greyed out
        EXPECTED: "Sorry but your credit/debit card is expired. Please edit expiry date or click *here* to register a new card" message and info (i) red icon are shown above the credit card placeholder/dropdown
        EXPECTED: ![](index.php?/attachments/get/36331) ![](index.php?/attachments/get/36332)
        EXPECTED: WHERE *here* is a tappable/clickable link-label, that redirects user to Account One - Deposit section, closing 'Quick Deposit' section once tapped/clicked.
        """
        pass

    def test_003_select_an_unexpired_card_in_credit_card_dropdown(self):
        """
        DESCRIPTION: Select **an unexpired card** in Credit Card Dropdown
        EXPECTED: Warning message disappears
        """
        pass

    def test_004_navigate_to_account_one_portal__deposit_page_via_right_menu__deposit_menu_item(self):
        """
        DESCRIPTION: Navigate to 'Account One' portal > 'Deposit' page (via 'Right' menu > 'Deposit' menu item)
        EXPECTED: 'Account One' portal is opened
        """
        pass

    def test_005_edit_expiry_date_of_an_expired_card_without_deposits_on_record(self):
        """
        DESCRIPTION: Edit expiry date of **an expired card without deposits on record**
        EXPECTED: Expiry date changes
        """
        pass

    def test_006_navigate_back_to_an_app(self):
        """
        DESCRIPTION: Navigate back to an app
        EXPECTED: 
        """
        pass

    def test_007___open_right_menu__tap_on_deposit_button__select_the_card_from_step_5(self):
        """
        DESCRIPTION: - Open 'Right' menu > tap on 'Deposit' button
        DESCRIPTION: - Select the card from step 5
        EXPECTED: - 'Deposit' button is disabled
        EXPECTED: - No warning messages being shown
        """
        pass

    def test_008_enter_valid_values_into_cvv__deposit_amount_fields(self):
        """
        DESCRIPTION: Enter valid values into 'CVV' & 'Deposit Amount' fields
        EXPECTED: - 'CVV' & 'Deposit Amount' fields are populated with entered values
        EXPECTED: - 'Deposit' button is enabled
        """
        pass

    def test_009_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: The deposit is successful
        """
        pass
