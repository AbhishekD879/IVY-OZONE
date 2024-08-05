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
class Test_C1663833_Payment_Methods_displaying_in_application_depending_on_CMS_configuration(Common):
    """
    TR_ID: C1663833
    NAME: Payment Methods displaying in application depending on CMS configuration
    DESCRIPTION: This test case verifies Payment Methods displaying in application depending on CMS configuration
    DESCRIPTION: Note: cannot automate as it requires changing/deleting payment methods in CMS and that can affect other tests and users
    PRECONDITIONS: 1. User is logged into application
    PRECONDITIONS: 2. CMS user is logged into CMS
    """
    keep_browser_open = True

    def test_001_1_in_oxygen_application_go_to_deposit_section2_verify_available_payment_methods_displaying_and_their_order(self):
        """
        DESCRIPTION: 1. In Oxygen application go to Deposit section
        DESCRIPTION: 2. Verify available Payment Methods displaying and their order
        EXPECTED: - Payment Methods that are configured in CMS and with Active = true are displaying
        EXPECTED: - Methods ordering is the same as in CMS Payment Listing
        """
        pass

    def test_002_1_navigate_to_cms___payments2_change_payment_methods_ordering3_navigate_back_to_application_deposit_section_and_verify_payment_methods_order(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Change Payment Methods ordering
        DESCRIPTION: 3. Navigate back to application (Deposit section) and verify Payment Methods order
        EXPECTED: - User is able to change order of Payment Methods (dragging chosen record to the needed row)
        EXPECTED: - Made changes are Saved immediately and message 'New Payment Method Order Saved!! OK!' appears
        EXPECTED: - Payment Methods are displaying properly based on ordering set via CMS
        """
        pass

    def test_003_1_navigate_to_cms___payments2_select_any_payment_method_with_active__true3_click_on_edit_button_and_uncheck_active_checkbox4_save_made_changes_confirmation_message___yes5_go_back_to_oxygen_application___deposit_section(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Select any Payment Method with Active = true
        DESCRIPTION: 3. Click on Edit button and uncheck Active checkbox
        DESCRIPTION: 4. Save made changes (Confirmation message -> Yes)
        DESCRIPTION: 5. Go back to Oxygen application -> Deposit section
        EXPECTED: - 'Payment Method Saving' message appears and Payment Method is disabled (Active = false) corresponding icon is displaying in 'Active' column
        EXPECTED: - In application (Deposit section) the Payment Methods with Active = false are not displaying
        """
        pass

    def test_004_1_navigate_to_cms___payments2_select_any_payment_method_with_active__true3_click_on_edit_button_and_uncheck_active_checkbox4_save_made_changes_confirmation_message___no5_go_back_to_oxygen_application___deposit_section(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Select any Payment Method with Active = true
        DESCRIPTION: 3. Click on Edit button and uncheck Active checkbox
        DESCRIPTION: 4. Save made changes (Confirmation message -> No)
        DESCRIPTION: 5. Go back to Oxygen application -> Deposit section
        EXPECTED: - Changes are discarded and and Payment Method is not updated (Active = true)
        EXPECTED: - Corresponding Payment Method is displaying properly in Oxygen application
        """
        pass

    def test_005_1_navigate_to_cms___payments2_select_payment_method_with_active__false3_click_on_edit_button_and_check_active_checkbox4_save_made_changes_confirmation_message___yes5_go_back_to_oxygen_application___deposit_section(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Select Payment Method with Active = false
        DESCRIPTION: 3. Click on Edit button and check Active checkbox
        DESCRIPTION: 4. Save made changes (Confirmation message -> Yes)
        DESCRIPTION: 5. Go back to Oxygen application -> Deposit section
        EXPECTED: - 'Payment Method Saving' message appears and Payment Method is enabled (Active = true) corresponding icon is displaying in 'Active' column
        EXPECTED: - In application (Deposit section) corresponding Payment Method with Active = active starts displaying properly after page refreshing
        """
        pass

    def test_006_1_navigate_to_cms___payments2_click_on_create_new_payment_method_button3_fill_in_payment_method_name_field_mandatory4_click_on_save_button5_go_back_to_oxygen_application___deposit_section(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Click on Create New Payment Method button
        DESCRIPTION: 3. Fill in Payment Method Name field (mandatory)
        DESCRIPTION: 4. Click on Save button
        DESCRIPTION: 5. Go back to Oxygen application -> Deposit section
        EXPECTED: - Payment Method is created with Active = false
        EXPECTED: - Payment Method Edit form is opened where Name field is prefilled with previously entered input (Payment Method Name) and Identifier (required field) is not set
        EXPECTED: - Created Payment Method is not displaying in Oxygen application
        """
        pass

    def test_007_1_navigate_to_cms___payments2_click_on_create_new_payment_method_button3_fill_in_payment_method_name_field_mandatory4_click_on_save_button5_select_identifier_that_is_not_used_for_other_payment_methods6_save_made_changes_confirmation_message___yes(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Click on Create New Payment Method button.
        DESCRIPTION: 3. Fill in Payment Method Name field (mandatory).
        DESCRIPTION: 4. Click on Save button
        DESCRIPTION: 5. Select Identifier that is not used for other Payment Methods
        DESCRIPTION: 6. Save made changes (Confirmation message -> Yes)
        EXPECTED: - 'Payment Method Saving' message appears and Payment Method is successfully created (Active = false) corresponding icon is displaying in 'Active' column
        EXPECTED: - Created Payment Method is not displaying in Oxygen application as Active = false
        """
        pass

    def test_008_1_navigate_to_cms___payments2_click_on_create_new_payment_method_button3_fill_in_payment_method_name_field_mandatory4_click_on_save_button5_select_identifier_that_is_used_for_other_payment_methods6_save_made_changes_confirmation_message___yes(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Click on Create New Payment Method button
        DESCRIPTION: 3. Fill in Payment Method Name field (mandatory)
        DESCRIPTION: 4. Click on Save button
        DESCRIPTION: 5. Select Identifier that is used for other Payment Method(s)
        DESCRIPTION: 6. Save made changes (Confirmation message -> Yes)
        EXPECTED: - Warning message 'There are more identifiers setup for ______, Please take a look to _____' appears but user is able to Save such Payment Method
        EXPECTED: - 'Payment Method Saving' message appears and Payment Method is successfully created (Active = false) corresponding icon is displaying in 'Active' column
        EXPECTED: - Created Payment Method is not displaying in Oxygen application as Active = false
        """
        pass

    def test_009_1_navigate_to_cms___payments2_select_any_payment_method_record_with_status__active3_click_on_delete_button_confirmation___yes4_go_back_to_oxygen_application___deposit_section(self):
        """
        DESCRIPTION: 1. Navigate to CMS -> Payments
        DESCRIPTION: 2. Select any Payment Method record with Status = Active
        DESCRIPTION: 3. Click on Delete button (Confirmation -> Yes)
        DESCRIPTION: 4. Go back to Oxygen application -> Deposit section
        EXPECTED: - Payment Method is successfully removed and grid is correspondingly updated
        EXPECTED: - Deleted Payment Method is not displaying in Oxygen application (Deposit section)
        """
        pass
