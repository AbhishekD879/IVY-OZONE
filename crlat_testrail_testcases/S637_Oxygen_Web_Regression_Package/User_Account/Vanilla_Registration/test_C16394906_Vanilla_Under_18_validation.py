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
class Test_C16394906_Vanilla_Under_18_validation(Common):
    """
    TR_ID: C16394906
    NAME: [Vanilla] Under 18 validation
    DESCRIPTION: This test case verifies whether it is possible to register a user who is not 18 years old yet
    PRECONDITIONS: User is logged out.
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

    def test_003_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
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

    def test_005_dont_select_any_information_in_the_date_of_birth_field(self):
        """
        DESCRIPTION: Don't select any information in the 'Date of Birth' field
        EXPECTED: 
        """
        pass

    def test_006_fill_in_the_rest_fields_of_the_page_and_tap_on_continue_button(self):
        """
        DESCRIPTION: Fill in the rest fields of the page and tap on 'Continue' button
        EXPECTED: - Warning message appears *'Please provide your date of birth'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        pass

    def test_007_enter_invalid_date_of_birth_and_repeat_step_6eg_default_value_daymonthyear_should_be_left_for_one_of_drop_down(self):
        """
        DESCRIPTION: Enter invalid 'Date of Birth' and repeat step 6
        DESCRIPTION: (e.g.: default value 'Day'/'Month'/'Year' should be left for one of drop down)
        EXPECTED: - Warning message appears *'Please provide your date of birth'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        pass

    def test_008_enter_date_of_birth_which_does_not_satisfy_criteria_of_18_years_old_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter 'Date of Birth' which does NOT satisfy criteria of 18 years old and repeat step 6
        EXPECTED: - Warning message appears *'You must be over 18 to create an account'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        pass

    def test_009_enter_such_date_of_birth_as_if_a_user_has_hisher_birthday_tomorrow_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter such 'Date of Birth' as if a user has his/her birthday tomorrow and repeat step 6
        EXPECTED: - Warning message appears *'You must be over 18 to create an account'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        pass

    def test_010_enter_18plus_date_of_birth_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter 18+ 'Date of Birth' and repeat step 6
        EXPECTED: User is navigated to the Page 3 successfully
        """
        pass
