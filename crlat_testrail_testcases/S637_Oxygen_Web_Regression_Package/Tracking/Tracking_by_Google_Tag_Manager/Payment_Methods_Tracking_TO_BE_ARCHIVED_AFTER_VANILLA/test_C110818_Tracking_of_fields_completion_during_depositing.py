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
class Test_C110818_Tracking_of_fields_completion_during_depositing(Common):
    """
    TR_ID: C110818
    NAME: Tracking of fields completion during depositing
    DESCRIPTION: This test case verifies tracking of fields completion during depositing
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=GA&title=Coral+Deposit+Journey
    PRECONDITIONS: 1. User is logged in to Oxygen application
    PRECONDITIONS: 2. User has the following cards: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: 3. User has Netteler and PayPal accounts
    PRECONDITIONS: 4. Browser console is opened
    PRECONDITIONS: 5. Test case should be run on Mobile, Tablet and Desktop
    """
    keep_browser_open = True

    def test_001_go_to_my_account___deposit_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Deposit' page
        EXPECTED: - 'Deposit' page is opened
        EXPECTED: - 'My Payments' tab is selected by default
        """
        pass

    def test_002_verify_fields_completion_during_depositing_via_visa_card(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Visa** card
        EXPECTED: 
        """
        pass

    def test_003_verify_completion_of_cv2_field(self):
        """
        DESCRIPTION: Verify completion of **CV2** field
        EXPECTED: 
        """
        pass

    def test_004_enter_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter valid CV2 into 'CV2' field
        EXPECTED: Entered value is shown in 'CV2' field
        """
        pass

    def test_005_type_in_console_datalayer_press_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **dataLayer**, press 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_006_expand_the_last_object(self):
        """
        DESCRIPTION: Expand the last Object
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventLabel' : '<<<field name>>>',
        EXPECTED: 'gtm.uniqueEventId': 16
        EXPECTED: 'paymentMethod' : '<<<payment method>>>',
        EXPECTED: 'location' : '<<<location>>>' }
        EXPECTED: );
        """
        pass

    def test_007_verify_field_name_parameter(self):
        """
        DESCRIPTION: Verify <<<field name>>> parameter
        EXPECTED: Field name is equal the name of the label of the field
        """
        pass

    def test_008_verify_payment_method_parameter(self):
        """
        DESCRIPTION: Verify <<<payment method>>> parameter
        EXPECTED: Payment method is equal to the the payment method used:
        EXPECTED: - 'credit card' - for Visa, Visa Electron, Master Card and Maestro cards;
        EXPECTED: - 'paypal' - for PayPal;
        EXPECTED: - 'neteller' - for Neteller.
        """
        pass

    def test_009_verify_location_parameter(self):
        """
        DESCRIPTION: Verify <<<location>>> parameter
        EXPECTED: Location is equal where the customer is depositing from:
        EXPECTED: - 'my account' - for the 'Deposit' page;
        EXPECTED: - 'betslip' - for the 'Quick Deposit' on Betslip.
        """
        pass

    def test_010_verify_completion_of_expiry_date_mmyy_fields(self):
        """
        DESCRIPTION: Verify completion of **Expiry Date (MM/YY)** fields
        EXPECTED: 
        """
        pass

    def test_011_click_edit_link_near_expiration_date(self):
        """
        DESCRIPTION: Click 'Edit' link near expiration date
        EXPECTED: Fields for changing month and year are shown
        """
        pass

    def test_012_select_different_value_for_month(self):
        """
        DESCRIPTION: Select different value for month
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_014_select_different_value_for_year(self):
        """
        DESCRIPTION: Select different value for year
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_016_verify_completion_of_enter_amount_field(self):
        """
        DESCRIPTION: Verify completion of **Enter Amount** field
        EXPECTED: 
        """
        pass

    def test_017_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons.
        EXPECTED: 
        """
        pass

    def test_018_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_019_verify_fields_completion_during_depositing_via_master_card_card_on_my_payments_tab_on_deposit_page(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Master Card** card on 'My Payments' tab on 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_020_repeat_steps_3_12(self):
        """
        DESCRIPTION: Repeat steps #3-12
        EXPECTED: 
        """
        pass

    def test_021_verify_fields_completion_during_depositing_via_maestro_card_on_my_payments_tab_on_deposit_page(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Maestro** card on 'My Payments' tab on 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_022_repeat_steps_3_12(self):
        """
        DESCRIPTION: Repeat steps #3-12
        EXPECTED: 
        """
        pass

    def test_023_verify_fields_completion_during_depositing_via_visa_electron_card_on_my_payments_tab_on_deposit_page(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Visa Electron** card on 'My Payments' tab on 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_024_repeat_steps_3_12(self):
        """
        DESCRIPTION: Repeat steps #3-12
        EXPECTED: 
        """
        pass

    def test_025_verify_fields_completion_during_depositing_via_neteller_on_my_payments_tab_on_deposit_page(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Neteller** on 'My Payments' tab on 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_026_verify_completion_of_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Verify completion of **Secure ID or Authentication Code** field
        EXPECTED: 
        """
        pass

    def test_027_enter_valid_secure_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter valid Secure ID into 'Secure ID or Authentication Code' field
        EXPECTED: Entered value is shown in 'Secure ID or Authentication Code' field
        """
        pass

    def test_028_repeat_steps_5_12(self):
        """
        DESCRIPTION: Repeat steps #5-12
        EXPECTED: 
        """
        pass

    def test_029_verify_fields_completion_during_depositing_via_paypal_on_my_payments_tab_on_deposit_page(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **PayPal** on 'My Payments' tab on 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_030_verify_completion_of_enter_amount_field(self):
        """
        DESCRIPTION: Verify completion of **Enter Amount** field
        EXPECTED: 
        """
        pass

    def test_031_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: 
        """
        pass

    def test_032_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_033_verify_fields_completion_during_depositing_via_paypal_on_add_paypal_tab(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **PayPal** on 'Add PayPal' tab
        EXPECTED: 
        """
        pass

    def test_034_repeat_steps_24_26(self):
        """
        DESCRIPTION: Repeat steps #24-26
        EXPECTED: 
        """
        pass

    def test_035_verify_fields_completion_during_depositing_via_neteller_on_add_neteller_tab(self):
        """
        DESCRIPTION: Verify fields completion during depositing via **Neteller** on 'Add NETELLER' tab
        EXPECTED: 
        """
        pass

    def test_036_verify_completion_of_account_idemail_field(self):
        """
        DESCRIPTION: Verify completion of **Account ID/Email** field
        EXPECTED: 
        """
        pass

    def test_037_enter_valid_account_id_into_account_idemail_field(self):
        """
        DESCRIPTION: Enter valid Account ID into 'Account ID/Email' field
        EXPECTED: 
        """
        pass

    def test_038_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_039_verify_completion_of_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Verify completion of **Secure ID or Authentication Code** field
        EXPECTED: 
        """
        pass

    def test_040_enter_valid_secure_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter valid Secure ID into 'Secure ID or Authentication Code' field
        EXPECTED: 
        """
        pass

    def test_041_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_042_verify_completion_of_enter_amount_field(self):
        """
        DESCRIPTION: Verify completion of **Enter Amount** field
        EXPECTED: 
        """
        pass

    def test_043_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: 
        """
        pass

    def test_044_repeat_steps_5_9(self):
        """
        DESCRIPTION: Repeat steps #5-9
        EXPECTED: 
        """
        pass

    def test_045_verify_fields_completion_during_depositing_from_quick_deposit_on_betslip(self):
        """
        DESCRIPTION: Verify fields completion during depositing from **Quick Deposit** on Betslip
        EXPECTED: 
        """
        pass

    def test_046_add_selection_to_betslipenter_amount_of_money_that_exceeds_user_balancetap_bet_now_button(self):
        """
        DESCRIPTION: Add selection to Betslip.
        DESCRIPTION: Enter amount of money that exceeds user balance.
        DESCRIPTION: Tap 'Bet Now' button.
        EXPECTED: 'Quick Deposit' is shown below bet line
        """
        pass

    def test_047_select_visa_cardrepeat_steps_3_24(self):
        """
        DESCRIPTION: Select **Visa** card.
        DESCRIPTION: Repeat steps #3-24
        EXPECTED: 
        """
        pass
