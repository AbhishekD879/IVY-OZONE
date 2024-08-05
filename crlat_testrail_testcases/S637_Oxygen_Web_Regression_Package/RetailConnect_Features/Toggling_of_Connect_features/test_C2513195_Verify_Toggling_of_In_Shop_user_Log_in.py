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
class Test_C2513195_Verify_Toggling_of_In_Shop_user_Log_in(Common):
    """
    TR_ID: C2513195
    NAME: Verify Toggling of In-Shop user Log in
    DESCRIPTION: This test case verify that In-Shop User Log In feature can be switched on/off in CMS
    DESCRIPTION: CMS -> System configuration -> Connect -> login
    PRECONDITIONS: 1. Load CMS and make sure In-Shop User Log In feature is turned off: System configuration -> Connect -> login = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    """
    keep_browser_open = True

    def test_001__tap_log_in_button(self):
        """
        DESCRIPTION: * Tap 'Log In' button
        EXPECTED: * 'Log In' dialog in opened
        """
        pass

    def test_002_verify_labels_on_log_in_form(self):
        """
        DESCRIPTION: Verify labels on Log In form
        EXPECTED: * 'Username' label
        EXPECTED: * Username Entry field
        EXPECTED: * 'Remember username' tick box
        EXPECTED: * 'Password' label
        EXPECTED: * Password Entry field
        EXPECTED: * 'Remember me' tick box
        """
        pass

    def test_003_try_to_log_in_with_16_digit_valid_connect_card_number_and_4_digit_valid_pin5000000000980347_1234(self):
        """
        DESCRIPTION: Try to log in with 16-digit valid Connect Card number and 4-digit valid PIN
        DESCRIPTION: (5000000000980347/ 1234)
        EXPECTED: * After tapping 'Log in' button "Unknown password you have entered. ......." error is shown
        """
        pass

    def test_004__go_to_cms_turn_in_shop_user_log_in_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Go to CMS
        DESCRIPTION: * Turn 'In-Shop User Log In' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_005__tap_log_in_button(self):
        """
        DESCRIPTION: * Tap 'Log In' button
        EXPECTED: * 'Log In' dialog in opened
        """
        pass

    def test_006_verify_labels_on_log_in_form(self):
        """
        DESCRIPTION: Verify labels on Log In form
        EXPECTED: * 'Enter your coral online username or your Connect Card number' label
        EXPECTED: * Username/Card Entry field
        EXPECTED: * 'Remember username or Connect Card number' tick box
        EXPECTED: * 'Password or 4-digit pin' label
        EXPECTED: * Password/PIN Entry field
        EXPECTED: * 'Remember me' tick box
        """
        pass

    def test_007_try_to_log_in_with_16_digit_valid_connect_card_number_and_4_digit_valid_pin5000000000980347_1234(self):
        """
        DESCRIPTION: Try to log in with 16-digit valid Connect Card number and 4-digit valid PIN
        DESCRIPTION: (5000000000980347/ 1234)
        EXPECTED: User is Logged in successfully
        """
        pass
