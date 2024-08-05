import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


# @pytest.mark.prod
# @pytest.mark.uat
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870148_Verify_user_can_use_help_line_chats_using_help_Contact_us_links(Common):
    """
    TR_ID: C44870148
    NAME: Verify user can use help line chats using help/Contact us links
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_000_pre_condition(self):
        """
        DESCRIPTION: User is logged in
        """
        self.site.login()

    def test_001_clicktap_my_account_button_avatar(self):
        """
        DESCRIPTION: Click/tap My Account button (Avatar)
        EXPECTED: For Mobile: Menu overlay is displayed with list of items
        EXPECTED: For Desktop: Right menu is displayed with list of items
        """
        self.site.wait_content_state('HomePage')
        self.site.header.right_menu_button.click()
        actual_right_menu_items = self.site.right_menu.items_names
        self.assertEqual(actual_right_menu_items, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU,
                         msg=f'Actual list: "{actual_right_menu_items}" is not same as Expected list: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        actual_deposit = [self.site.right_menu.deposit_button.text]
        self.assertEqual(actual_deposit, [vec.bma.RIGHT_MENU_DEPOSIT],
                         msg=f'Actual list: "{actual_deposit}" is not same as Expected list: "{[vec.bma.RIGHT_MENU_DEPOSIT]}"')

    def test_002_clicktap_help__contact_menu_option(self):
        """
        DESCRIPTION: Click/tap Help & Contact menu option
        EXPECTED: User is taken to Help & Contact page
        EXPECTED: Target URL - https://sports.coral.co.uk/en/mobileportal/contact
        """
        self.site.right_menu.click_item('Help & Contact')
        wait_for_result(lambda: self.site.direct_chat.topics, timeout=15)
        actual_url = self.device.get_current_url()
        expected_url = "https://" + tests.HOSTNAME + "/en/mobileportal/contact"
        self.assertEqual(actual_url, expected_url,
                         msg=f'Actual url: "{actual_url}" is not same as Expected url: "{expected_url}"')

    def test_003_verify_topics_displayed(self):
        """
        DESCRIPTION: Verify topics displayed
        EXPECTED: Account Access
        EXPECTED: Promotions & Bonuses
        EXPECTED: Bingo
        EXPECTED: Poker
        EXPECTED: Deposit
        EXPECTED: Withdraw
        EXPECTED: Account Details & Verification
        EXPECTED: Sports Rules
        EXPECTED: Technical Issues
        EXPECTED: Responsible Gambling
        """
        # covered in step 4

    def test_004_select_any_topics_exaccount_access(self):
        """
        DESCRIPTION: Select any Topics, Ex.Account Access
        EXPECTED: Selected topic's subcategory options are displayed
        """
        topics_list = self.site.direct_chat.topics.items_as_ordered_dict
        for topic in range(len(topics_list.keys())):
            topics_name, topics = list(topics_list.items())[topic]
            self.assertIn(topics_name, vec.bma.LIST_OF_HELP_AND_CONTACT, msg=f'"{topics_name}" is not displayed')
            topics.click()
            sleep(1.5)
            sub_categories = self.site.direct_chat.subcategory.items_as_ordered_dict
            self.assertTrue(sub_categories.values(), msg='Sub Category options are not displayed')
        topics = list(topics_list.values())[0]
        topics.click()
        sleep(1.5)

    def test_005_select_any_option_from_the_subcategory_list(self):
        """
        DESCRIPTION: Select any option from the subcategory list
        EXPECTED: "Yes" and "No" buttons are displayed
        """
        sub_categories = self.site.direct_chat.subcategory.items_as_ordered_dict
        sub_category = list(sub_categories.values())[0]
        sub_category.click()
        self.assertTrue(self.site.direct_chat.yes_button.is_displayed(), msg='"Yes" button is not present')
        self.assertTrue(self.site.direct_chat.no_button.is_displayed(), msg='"No" button is not present')

    def test_006_click_on_yes_button(self):
        """
        DESCRIPTION: Click on Yes button
        EXPECTED: My Account Details page is opened.
        EXPECTED: Live chat
        EXPECTED: Email
        EXPECTED: Visit our Help pages
        EXPECTED: Verify your details are displayed
        """
        self.site.direct_chat.yes_button.click()
        for name in list(self.site.direct_chat.chat_options.keys()):
            self.assertTrue(name in vec.bma.LIVE_CHAT_PAGE_OPTIONS, msg=f'"{name}" is not displayed')
        verify_details_text = self.site.direct_chat.verify_details.text.split('\n')[0]
        self.assertEqual(verify_details_text, "Verify your details",
                         msg=f'Actual text: "{verify_details_text}" is not same as Expected text "Verify your details"')

    def test_007_tap_on_live_chat_tab(self):
        """
        DESCRIPTION: Tap on 'Live chat' tab
        EXPECTED: User is navigated to "Live Chat" Page
        EXPECTED: Header with "Live Chat", minimise and close button are available
        EXPECTED: "You're one step away from talking to one of our experts, they'll be with you shortly." message is displayed.(if applicable)
        """
        live_chat = list(self.site.direct_chat.chat_options.values())[0]
        live_chat.click()
        header = self.site.direct_chat.header
        self.assertEqual(header.title, vec.bma.LIVE_CHAT_HEADER_TITLE,
                         msg=f'Actual title: "{header.title}" is not same as Expected title: "{vec.bma.LIVE_CHAT_HEADER_TITLE}"')
        self.assertTrue(header.has_close_button(), msg='"Close button" is not available')
        self.assertTrue(header.has_toggle_button(), msg='"Toggle button" is not available')
        actual_live_chat_text = self.site.direct_chat.live_chat_text_verification.text
        self.assertEqual(actual_live_chat_text, vec.bma.LIVE_CHAT_TEXT,
                         msg=f'Actual text: "{actual_live_chat_text}" is not same as Expected text: "{vec.bma.LIVE_CHAT_TEXT}"')

    def test_008_live_chat_is_active(self):
        """
        DESCRIPTION: Live chat is active
        EXPECTED: Wait until "Welcome 'username' to Coral Chat!" is displayed
        """
        wait_for_result(lambda: self.site.direct_chat.agent_name_verification, timeout=90)
        agent_name = self.site.direct_chat.agent_name_verification.text
        self.assertIn("has joined the chat", agent_name, msg='Name of the agent is not displayed')
        welcome_text = self.site.direct_chat.welcome_text_verification.text
        self.assertTrue(welcome_text.startswith("Welcome") and welcome_text.endswith("Chat!"), msg='Welcome text is not displayed')

    def test_009_click_on_close_button(self):
        """
        DESCRIPTION: Click on Close Button
        EXPECTED: "You are about to terminate this Live Help. Are you sure you got the answer to your question?" message is displayed.
        EXPECTED: "Cancel" and "Close Chat" button are displayed
        """
        self.site.direct_chat.header.close_button.click()
        actual_message = self.site.direct_chat.header.confirmation_text
        self.assertEqual(actual_message, vec.bma.CLOSE_CHAT_CONFIRMATION,
                         msg=f'Actual message: "{actual_message}" is not same as Expected message: "{vec.bma.CLOSE_CHAT_CONFIRMATION}"')
        self.assertTrue(self.site.direct_chat.header.cancel_button.is_displayed(), msg='"Cancel" button is not displayed')
        self.assertTrue(self.site.direct_chat.header.close_chat_button.is_displayed(), msg='"Close Chat" button is not displayed')

    def test_010_tap_on_close_chat_button(self):
        """
        DESCRIPTION: Tap on Close Chat Button
        EXPECTED: User is on My Account Details Page
        """
        self.site.direct_chat.header.close_chat_button.click()
        for name in list(self.site.direct_chat.chat_options.keys()):
            self.assertTrue(name in vec.bma.LIVE_CHAT_PAGE_OPTIONS, msg=f'"{name}" is not displayed')
        verify_details_text = self.site.direct_chat.verify_details.text.split('\n')[0]
        self.assertEqual(verify_details_text, "Verify your details",
                         msg=f'Actual text: "{verify_details_text}" is not same as Expected text "Verify your details"')
