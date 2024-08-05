import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.desktop
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17995881_Vanilla_Verify_Messages_right_menu_option(Common):
    """
    TR_ID: C17995881
    NAME: [Vanilla] Verify Messages right menu option
    DESCRIPTION: This test case is to verify Messages right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env(self):
        """
        DESCRIPTION: Log in to test env
        EXPECTED: User is logged in, My Account button appears
        """
        self.site.login()
        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='My Account button is not displayed after user logged in')

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Right Menu is not displayed')

    def test_003_clicktap_messages_menu_option(self):
        """
        DESCRIPTION: Click/tap Messages menu option
        EXPECTED: My Messages pop-up is displayed with the list of user's messages
        """
        self.site.right_menu.click_item(
            vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3] if self.brand == 'bma' else vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[5])
        self.site.wait_content_state_changed()
        actual_title_text = self.site.messages.title.text
        Expected_text = vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3] if self.brand == 'bma' else vec.bma.MY_INBOX
        self.assertEqual(actual_title_text, Expected_text,
                         msg=f'Actual text: "{actual_title_text}" is not equal with the'
                             f'Expected text: "{Expected_text}"')

        self.site.wait_splash_to_hide(timeout=1)
        if self.site.messages.no_messages_text is not None:
            actual_title_text = self.site.messages.no_messages_text.text
            self.assertEqual(actual_title_text, vec.bma.NO_MESSAGES,
                             msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                 f'Expected text: "{vec.bma.NO_MESSAGES}"')
        else:
            self.assertTrue(self.site.messages.message_details.is_displayed(), msg="Message is not displayed")
