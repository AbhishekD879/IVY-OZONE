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
class Test_C13828771_Ladbrokes_Verify_happy_KYC_verification_journey_after_registration(Common):
    """
    TR_ID: C13828771
    NAME: Ladbrokes. Verify happy KYC verification journey after registration
    DESCRIPTION: This test case verifies that a new user (IMS.AVR = 'Under review') can continue using the app after registration
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. App is loaded
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS:
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_mobiletap_loginjoin_button__join_us_here_buttondesktopclick_join_now_buttonfor_ladbrokes_mobile_and_desktopclick_on_register_button(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap 'Login/Join' button > 'Join us here' button
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click 'Join now' button
        DESCRIPTION: **For Ladbrokes (Mobile and Desktop)**:
        DESCRIPTION: Click on 'Register' button
        EXPECTED: Account One Registration page is displayed
        """
        pass

    def test_002_complete_the_3_step_registration_processand_tap_the_button_open_accountfor_test_env_email__testplaytechcom(self):
        """
        DESCRIPTION: Complete the 3 step registration process
        DESCRIPTION: and tap the button 'Open account'
        DESCRIPTION: (for test env. 'email' = "test@playtech.com")
        EXPECTED: 'Save my preferences' page is opened
        """
        pass

    def test_003_before_a_user_is_auto_logged_inin_ims__find_a_just_registered_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' to "Under review"
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_004_fill_the_contact_preference_page__tap_save_my_preferences_button(self):
        """
        DESCRIPTION: Fill the 'Contact Preference Page' > tap 'Save my preferences' button
        EXPECTED: **Mobile:**
        EXPECTED: Account One Deposit page is displayed
        EXPECTED: **Desktop:**
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged in with registered credentials
        """
        pass

    def test_005_close_account_one_deposit_page(self):
        """
        DESCRIPTION: Close 'Account One Deposit' page
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged in with registered credentials
        EXPECTED: * User can browse the app without any restrictions
        """
        pass
