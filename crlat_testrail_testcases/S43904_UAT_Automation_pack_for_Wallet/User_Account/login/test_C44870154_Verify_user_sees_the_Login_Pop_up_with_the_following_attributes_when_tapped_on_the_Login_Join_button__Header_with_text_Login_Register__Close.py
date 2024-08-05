import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870154_Verify_user_sees_the_Login_Pop_up_with_the_following_attributes_when_tapped_on_the_Login_Join_button__Header_with_text_Login_Register__Close_button__Username_text_and_entry_area__Password_entry_and_entry_area_with_Show_text_Remember_M(Common):
    """
    TR_ID: C44870154
    NAME: ""Verify user sees the Login Pop up with the following attributes when tapped on the Login/Join button  - Header with text ""Login/Register""  - Close button - Username text and entry area  - Password entry and entry area with Show text Remember M
    DESCRIPTION: 
    PRECONDITIONS: User not logged in
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: 
        """
        pass

    def test_002_tap_on_log_in(self):
        """
        DESCRIPTION: Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: a)Online / b)Connect card
        EXPECTED: Options under Online
        EXPECTED: 1.Connect card
        EXPECTED: 2.Username
        EXPECTED: 3.Password
        EXPECTED: 4.Remember me check box
        EXPECTED: 5.Forgot Username
        EXPECTED: 6.Forgot Password
        EXPECTED: 7.Login
        EXPECTED: 8.Register
        EXPECTED: Under b)Connect card
        EXPECTED: 1. Connect card number
        EXPECTED: 2. 4 digit pin
        EXPECTED: 3. Remember me
        EXPECTED: 4. Forgot my 4 digit pin
        EXPECTED: 5. Login
        EXPECTED: 6. Register
        EXPECTED: On clicking 'REGISTER' the user is navigated to the registration page (Step 3)
        """
        pass

    def test_003_click_on_register_from_log_in_page_or_join_now_button_from_the_header(self):
        """
        DESCRIPTION: Click on 'REGISTER' from log in page or 'JOIN NOW' button from the header
        EXPECTED: Registration page is opened
        """
        pass

    def test_004_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: Country of residency
        EXPECTED: Currency
        EXPECTED: Email
        EXPECTED: Create Username
        EXPECTED: Create Password
        """
        pass

    def test_005_click_next_step_button(self):
        """
        DESCRIPTION: Click 'Next Step' button
        EXPECTED: Registration Step 2 is opened
        """
        pass

    def test_006_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: 1. Title - choose any option
        EXPECTED: 2. First name - random name
        EXPECTED: 3. Last name - random name
        EXPECTED: 4. Date of birth (random day/month/year, 18 years plus)
        """
        pass

    def test_007_click_next_step_button(self):
        """
        DESCRIPTION: Click 'Next Step' button
        EXPECTED: Registration Step 3 is opened
        """
        pass

    def test_008_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: 1. UK Postcode (random UK Postcode) - after the UK Post code is added, click on Find button in order to automatically populate the Address fields (PLEASE NOTE THAT VPN CONNECTION SHOULD BE TURNED ON)
        EXPECTED: 2. Mobile number (random number - you can use 0000000000)
        EXPECTED: 3. Select Marketing Preferences
        """
        pass

    def test_009_click_crete_my_account_button(self):
        """
        DESCRIPTION: Click 'Crete my account' button
        EXPECTED: Set your deposit limits page opened
        EXPECTED: 1. Select limits
        EXPECTED: 2. Tick- Fund Protection policy.
        """
        pass

    def test_010_click_submit_button__deposit_page_opened(self):
        """
        DESCRIPTION: Click 'Submit' button > 'Deposit' page opened
        EXPECTED: Tap 'Add Debit/Credit Cards' tab & select payment option page is displayed with following fields:
        EXPECTED: Enter Amount (- / +)
        EXPECTED: Cardholder Name
        EXPECTED: Card Number
        EXPECTED: Expiration Date
        EXPECTED: CVV
        """
        pass

    def test_011_clicktap_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'Deposit' button
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Amount on message is displayed in decimal format
        EXPECTED: User stays on the 'My Payments' tab for few seconds and then taken to home page
        """
        pass
