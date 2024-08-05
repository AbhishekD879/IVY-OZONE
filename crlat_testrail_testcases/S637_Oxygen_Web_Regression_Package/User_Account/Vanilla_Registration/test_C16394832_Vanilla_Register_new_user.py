import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C16394832_Vanilla_Register_new_user(Common):
    """
    TR_ID: C16394832
    NAME: [Vanilla] Register new user
    DESCRIPTION: This test case verifies possibility of new user registration.
    DESCRIPTION: Autotest [C25219966]
    PRECONDITIONS: Make sure you are logged out of the system.
    PRECONDITIONS: This test case should be tested on Desktop, Tablet and Mobile devices.
    PRECONDITIONS: - to skip KYC, username should start with **'testgvccl-'**; **@internalgvc.com** domain (see Confluence page - https://confluence.egalacoral.com/display/SPI/How+to+create+test+user+for+GVC+Vanilla+automatically+by-passing+KYC )
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: - A letter
    PRECONDITIONS: - A number
    PRECONDITIONS: - 6 to 20 characters
    PRECONDITIONS: - Must not contain parts of your name or e-mail
    PRECONDITIONS: - Must not contain any of these special characters (‘ “ < > & % )
    """
    keep_browser_open = True

    def test_001_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        EXPECTED: 
        """
        pass

    def test_002_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: Page 'Registration - Step 1 of 3' is shown
        """
        pass

    def test_003_enter_correct_data_to_all_required_fields_due_to_validation_rules__choose_country_of_residence__choose_currency_eurgbpusd__enter_your_email__create_username__create_password(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules:
        DESCRIPTION: - Choose **Country of residence**;
        DESCRIPTION: - Choose **Currency** (EUR/GBP/USD);
        DESCRIPTION: - Enter your **email**;
        DESCRIPTION: - Create **username**;
        DESCRIPTION: - Create **password**
        EXPECTED: - All mandatory fields are filled
        EXPECTED: - None of fields are highlighted in red
        """
        pass

    def test_004_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported
        EXPECTED: - Page 'Registration - Step 2 of 3' is shown
        """
        pass

    def test_005_enter_correct_data_to_all_required_fields_due_to_validation_rules__select_mr_or_ms__enter_your_first_name__enter_your_last_name__set_your_date_of_birth_from_dropdown(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules:
        DESCRIPTION: - Select **Mr.** or **Ms.**;
        DESCRIPTION: - Enter your **First Name**;
        DESCRIPTION: - Enter your **Last name**;
        DESCRIPTION: - Set your **Date of birth** from dropdown
        EXPECTED: - All mandatory fields are filled
        EXPECTED: - None of fields are highlighted in red
        """
        pass

    def test_006_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported
        EXPECTED: - Page 'Registration - Step 3 of 3' is shown
        """
        pass

    def test_007_tap_on_2_buttonindexphpattachmentsget33916(self):
        """
        DESCRIPTION: Tap on '2' button
        DESCRIPTION: ![](index.php?/attachments/get/33916)
        EXPECTED: - Page 'Registration - Step 2 of 3' is shown
        EXPECTED: - All previously entered data is saved and shown
        """
        pass

    def test_008_tap_on_1_buttonindexphpattachmentsget33921(self):
        """
        DESCRIPTION: Tap on '1' button
        DESCRIPTION: ![](index.php?/attachments/get/33921)
        EXPECTED: - Page 'Registration - Step 1 of 3' is shown
        EXPECTED: - All previously entered data is saved and shown
        """
        pass

    def test_009_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported
        EXPECTED: - Page 'Registration - Step 2 of 3' is shown
        """
        pass

    def test_010_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported
        EXPECTED: - Page 'Registration - Step 3 of 3' is shown
        """
        pass

    def test_011_enter_correct_data_to_all_required_fields_due_to_validation_rules__enter_postcode_or_first_line_of_addressa_after_entering_a_postcode_address_fields_are_expanded_automatically_in_dropdownb_is_an_option_to_enter_address_manually__country_code_is_set_by_default__provide_your_mobile_number__select_an_option_if_you_would_like_to_receive_freebets_bonuses_and_offers_from_coral(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules:
        DESCRIPTION: - **Enter postcode or first line of address**:
        DESCRIPTION: a) after entering a postcode, address fields are expanded automatically in dropdown;
        DESCRIPTION: b) is an option to enter address manually;
        DESCRIPTION: - **Country code** is set by default;
        DESCRIPTION: - Provide your **mobile number**;
        DESCRIPTION: - Select an option if you would like to receive FreeBets, bonuses and offers from Coral;
        EXPECTED: - Each field is validated and any validation issues are reported
        """
        pass

    def test_012_tap_on_create_my_account_button(self):
        """
        DESCRIPTION: Tap on 'Create my account' button
        EXPECTED: - **'Set your deposit limits'** page is shown
        """
        pass

    def test_013_select_suitable_limits_fieldfill_in_valid_information_for_all_required_registration_fields(self):
        """
        DESCRIPTION: Select suitable Limits field.
        DESCRIPTION: Fill in valid information for all required registration fields.
        EXPECTED: - All entered data is displayed correctly
        EXPECTED: - No error messages are displayed
        """
        pass

    def test_014_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: - **'Deposit'** page is shown
        EXPECTED: - pop-up is shown:
        EXPECTED: ![](index.php?/attachments/get/33925)
        """
        pass

    def test_015_click_on_x_button_at_the_top_right_corner_of_deposit_page(self):
        """
        DESCRIPTION: Click on 'X' button at the top right corner of 'Deposit' page
        EXPECTED: - User is redirected to the homepage
        """
        pass
