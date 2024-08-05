import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2088610_Verify_Upgrade_Page__Card_number_PIN(Common):
    """
    TR_ID: C2088610
    NAME: Verify Upgrade Page - Card number/PIN
    DESCRIPTION: This test case verify Upgrade Landing Page
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-2417 Upgrade Landing Page
    DESCRIPTION: HMN-3777 Web: Changes for Upgrade Pages
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: To see the first upgrade page with card number and pin, Local Storage should be cleared and the home page should be reloaded when an in-shop user is logged in:
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Log in with in-shop user (5000000000992185/ 1234)
    PRECONDITIONS: * Clear local storage -> reload page
    """
    keep_browser_open = True

    def test_001_chose_connect_from_header_ribbon(self):
        """
        DESCRIPTION: Chose 'Connect' from header ribbon
        EXPECTED: Connect landing page is opened
        """
        pass

    def test_002_tap_use_connect_online_buttonupdated_after_vanilla_migration_tab_upgrade_your_connect_account_to_be_online_button(self):
        """
        DESCRIPTION: Tap 'Use Connect Online' button
        DESCRIPTION: [Updated after vanilla migration:] Tab 'Upgrade your Connect account to be online' button
        EXPECTED: Upgrade Landing Page is opened
        """
        pass

    def test_003_verify_content_of_upgrade_landing_page(self):
        """
        DESCRIPTION: Verify content of Upgrade Landing Page
        EXPECTED: * [Before vanilla migration] 'Enter Coral Connect card details...' text correspond to CMS configurations (Static block 'Connect Marketing Upgrade')
        EXPECTED: * 'Card Number' field is divided into 4 block
        EXPECTED: * Hint 'Please enter your 16 digit Coral Connect card number'
        EXPECTED: * 'Pin number' field
        EXPECTED: * Hint 'Please enter your four digit Coral Connect pin'
        EXPECTED: * 'Confirm' button
        """
        pass

    def test_004_verify_card_number_field_validation(self):
        """
        DESCRIPTION: Verify 'Card Number' field validation
        EXPECTED: * Only Number characters can be entered
        EXPECTED: * Each block allows to enter only 4 characters
        EXPECTED: * After 4 characters are entered into one block next block becomes active
        """
        pass

    def test_005_verify_pin_number_field_validation(self):
        """
        DESCRIPTION: Verify 'Pin number' field validation
        EXPECTED: * Pin number' field becomes active after 'Card Number' field is filled completely
        EXPECTED: * Only 4 Number characters can be entered
        """
        pass

    def test_006_verify_confirm_button_availability(self):
        """
        DESCRIPTION: Verify 'Confirm' button availability
        EXPECTED: * 'Confirm' button becomes active after 'Card Number' and 'Pin number' are filled completely
        """
        pass

    def test_007_verify_validation_rules_after_tapping_confirm_button(self):
        """
        DESCRIPTION: Verify validation rules after tapping 'Confirm' button
        EXPECTED: * If entered Connect Card is not valid/ blocked then error message is displayed: 'Your card number appears to be entered incorrectly, please can you recheck the card number entered'
        EXPECTED: [After vanilla migration] The message is: 'There is an error message:"16-digit Connect Card number not recognised. Please check and try again.'
        EXPECTED: * If entered Connect card is Multi-Channel then error message is displayed saying that the account is already upgraded
        EXPECTED: * If entered PIN is not associated with entered Connect Card then error message is displayed saying that PIN is incorrect
        """
        pass

    def test_008_verify_successful_redirecting_to_following_page_after_tapping_confirm_button(self):
        """
        DESCRIPTION: Verify successful redirecting to following page after tapping 'Confirm' button
        EXPECTED: If entered Connect Card belongs to in-shop account and entered PIN is valid then user is redirected to next screen 'Enter Coral Connect details'
        """
        pass
