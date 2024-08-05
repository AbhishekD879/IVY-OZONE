import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C59498815_Verify_opening_of_My_Inbox_page(Common):
    """
    TR_ID: C59498815
    NAME: Verify opening of My Inbox page
    DESCRIPTION: This test case verifies opening of My Inbox page
    PRECONDITIONS: 1. User is logged in with valid credentials
    PRECONDITIONS: 2. 'Messages' menu item is configured in GVC CNS and is displayed in User Menu
    PRECONDITIONS: 3. 'My Inbox' icon is present in header
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 'Messages' item on the menu, 'My Inbox' icon in the header and 'My Inbox' overlay itself is managed on GVC side.
    """
    keep_browser_open = True

    def test_001_load_app_and_click_my_inbox_in_header(self):
        """
        DESCRIPTION: Load app and click My Inbox in header
        EXPECTED: * Overlay opens with 'My Inbox' title and Close (X) button.
        EXPECTED: * 'You have no messages!' message displayed is user has no messages
        EXPECTED: * List of messages displayed if user has any.
        """
        self.site.login(username=tests.settings.betplacement_user)
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.user_panel.my_inbox_button.is_displayed(),
                            msg='"Inbox button" is not displayed')
            self.site.header.user_panel.my_inbox_button.click()
            self.site.messages.close_button.click()
            self.site.wait_content_state('Homepage')

    def test_002_close_overlayopen_user_menu_and_click_messages(self):
        """
        DESCRIPTION: Close overlay.
        DESCRIPTION: Open User menu and click 'Messages'
        EXPECTED: * Overlay opens with 'My Inbox' title and Close (X) button.
        EXPECTED: * 'You have no messages!' message displayed is user has no messages
        EXPECTED: * List of messages displayed if user has any.
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Right menu is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])
            self.site.wait_content_state_changed()
            actual_title_text = self.site.messages.title.text
            self.assertEqual(actual_title_text, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3],
                             msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                 f'Expected text: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3]}"')
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[5])
            self.site.wait_content_state_changed()
            actual_title_text = self.site.messages.title.text
            self.assertEqual(actual_title_text, vec.bma.MY_INBOX,
                             msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                 f'Expected text: "{vec.bma.MY_INBOX}"')

        self.site.wait_splash_to_hide(timeout=1)
        if self.device_type == 'desktop':
            if self.site.messages.no_messages_text is not None:
                actual_title_text = self.site.messages.no_messages_text.text
                self.assertEqual(actual_title_text, vec.bma.NO_MESSAGES,
                                 msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                     f'Expected text: "{vec.bma.NO_MESSAGES}"')
            else:
                self.assertTrue(self.site.messages.message_details.is_displayed(), msg="Message is not displayed")
            self.assertTrue(self.site.messages.close_button.is_displayed(),
                            msg='"close button of message body" is not displayed')
            self.site.messages.close_button.click()
        else:
            if self.site.messages.no_messages_text is not None:
                actual_title_text = self.site.messages.no_messages_text.text
                self.assertEqual(actual_title_text, vec.bma.NO_MESSAGES,
                                 msg=f'Actual text: "{actual_title_text}" is not equal with the'
                                     f'Expected text: "{vec.bma.NO_MESSAGES}"')
            else:
                self.site.messages.message_expand.click()
                self.assertTrue(self.site.messages.message_details.is_displayed(), msg="Message is not displayed")
                self.assertTrue(self.site.messages.back_button.is_displayed(),
                                msg='"back button of message body" is not displayed')
                self.site.messages.back_button.click()
            self.assertTrue(self.site.messages.back_button.is_displayed(),
                            msg='"back button of message inbox" is not displayed')
            self.site.messages.back_button.click()
            self.assertTrue(self.site.right_menu.close_icon.is_displayed(),
                            msg='"close button of right menu" is not displayed')
            self.site.right_menu.close_icon.click()
        self.site.wait_content_state('Homepage')
