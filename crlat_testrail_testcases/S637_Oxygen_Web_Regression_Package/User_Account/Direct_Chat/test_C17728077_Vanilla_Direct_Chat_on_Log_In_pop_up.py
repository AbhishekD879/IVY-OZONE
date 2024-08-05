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
class Test_C17728077_Vanilla_Direct_Chat_on_Log_In_pop_up(Common):
    """
    TR_ID: C17728077
    NAME: [Vanilla] Direct Chat on Log In pop up
    DESCRIPTION: This test case verifies triggering Direct Chat on FORGOTTEN USERNAME and FORGOTTEN PASSWORD page
    PRECONDITIONS: Direct Chat should be tested on PROD endpoints
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_tap_on_loggin_button(self):
        """
        DESCRIPTION: Tap on LOGGIN button
        EXPECTED: LOGIN pop up appears
        """
        pass

    def test_003_tap_on_i_forgot_username_link(self):
        """
        DESCRIPTION: Tap on 'I forgot Username' link
        EXPECTED: FORGOTTEN USERNAME page is open and 'Live Chat' button is available
        """
        pass

    def test_004_tab_live_chat_button(self):
        """
        DESCRIPTION: Tab 'Live Chat' button
        EXPECTED: Live Chat welcome page is open
        """
        pass

    def test_005_type_name_and_email_and_tab_start_chat_button(self):
        """
        DESCRIPTION: Type Name and Email and tab 'START CHAT' button
        EXPECTED: Live Chat page is open
        """
        pass

    def test_006_type_a_message_and_tab_send_button(self):
        """
        DESCRIPTION: Type a message and tab 'SEND' button
        EXPECTED: Message is sent
        """
        pass

    def test_007_go_to_the_main_page_of_application_an_tab_login_button(self):
        """
        DESCRIPTION: Go to the main page of application an tab LOGIN button
        EXPECTED: LOGIN pop up appears
        """
        pass

    def test_008_tap_on_i_forgot_password_link(self):
        """
        DESCRIPTION: Tap on 'I forgot Password' link
        EXPECTED: FORGOTTEN PASSWORD page is open and 'Live Chat' button is available
        """
        pass

    def test_009_tab_live_chat_button(self):
        """
        DESCRIPTION: Tab 'Live Chat' button
        EXPECTED: Live Chat page is open
        """
        pass

    def test_010_type_a_message_and_tab_send_button(self):
        """
        DESCRIPTION: Type a message and tab 'SEND' button
        EXPECTED: Message is sent
        """
        pass
