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
class Test_C36533576_Users_Marketing_Preferences(Common):
    """
    TR_ID: C36533576
    NAME: User's Marketing Preferences
    DESCRIPTION: Verify that the customer can set Marketing Preferences through New Registration journey and see them in Settings afterwards
    DESCRIPTION: AUTOTEST [C45357161]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_click_on_join_button(self):
        """
        DESCRIPTION: Click on Join button
        EXPECTED: Registration Page 1 is loaded
        """
        pass

    def test_002_fill_in_the_required_data1_country_of_residence2_currency_type_for_the_user3_email_address4_username5_password9_click_on_continue_button(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Country of residence
        DESCRIPTION: 2. Currency type for the user
        DESCRIPTION: 3. Email address
        DESCRIPTION: 4. Username
        DESCRIPTION: 5. Password
        DESCRIPTION: 9. Click on "Continue" button
        EXPECTED: Registration Page 2 is opened
        """
        pass

    def test_003_fill_in_the_required_data1_choose_between_mr_and_ms2_first_name3_last_name4_date_of_birth5_click_on_continue_button(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Choose between Mr. and Ms.
        DESCRIPTION: 2. First name
        DESCRIPTION: 3. Last name
        DESCRIPTION: 4. Date of birth
        DESCRIPTION: 5. Click on 'Continue' button
        EXPECTED: Registration Page 3 is opened
        """
        pass

    def test_004_fill_in_the_required_data1_postcode_eg_123452_mobile_number3__all_the_checkboxes_with_marketing_preferences_indexphpattachmentsget17649989click_on_create_my_account_button(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Postcode (e.g. 12345)
        DESCRIPTION: 2. Mobile number
        DESCRIPTION: 3. ** All the checkboxes with Marketing Preferences **
        DESCRIPTION: ![](index.php?/attachments/get/17649989)
        DESCRIPTION: Click on 'Create my account' button
        EXPECTED: 'Set your deposit limits' page is opened
        """
        pass

    def test_005__choose_no_limit_option_for_the_user_put_a_tick_in_fund_protection_accepting_checkbox_press_on_submit_button(self):
        """
        DESCRIPTION: * Choose 'No limit option for the user'
        DESCRIPTION: * Put a tick in Fund Protection accepting checkbox
        DESCRIPTION: * Press on 'Submit' button
        EXPECTED: * 'You are registered!' green panel is displayed on Deposit page
        EXPECTED: * The customer is able to choose between available deposit methods
        """
        pass

    def test_006_close_the_deposit_dialogue_with_a_x_button(self):
        """
        DESCRIPTION: Close the Deposit dialogue with a 'X' button
        EXPECTED: User is redirected to the Homepage
        """
        pass

    def test_007_open_my_account_menu__settings__marketing_preferences(self):
        """
        DESCRIPTION: Open My Account menu > Settings > Marketing Preferences
        EXPECTED: * 'Communication preferences' page is opened
        EXPECTED: * All the checkboxes chosen in step 4 are still ticked
        EXPECTED: ![](index.php?/attachments/get/17649984)
        """
        pass
