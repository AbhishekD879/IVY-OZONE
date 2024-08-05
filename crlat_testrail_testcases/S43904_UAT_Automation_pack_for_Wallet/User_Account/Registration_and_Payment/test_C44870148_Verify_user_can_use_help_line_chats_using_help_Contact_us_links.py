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
class Test_C44870148_Verify_user_can_use_help_line_chats_using_help_Contact_us_links(Common):
    """
    TR_ID: C44870148
    NAME: Verify user can use help line chats using help/Contact us links
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_clicktap_my_account_button_avatar(self):
        """
        DESCRIPTION: Click/tap My Account button (Avatar)
        EXPECTED: For Mobile: Menu overlay is displayed with list of items
        EXPECTED: For Desktop: Right menu is displayed with list of items
        """
        pass

    def test_002_clicktap_help__contact_menu_option(self):
        """
        DESCRIPTION: Click/tap Help & Contact menu option
        EXPECTED: User is taken to Help & Contact page
        EXPECTED: Target URL - https://sports.coral.co.uk/en/mobileportal/contact
        """
        pass

    def test_003_verify_topics_displayed(self):
        """
        DESCRIPTION: Verify topics displayed
        EXPECTED: Shop closure FAQs
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
        pass

    def test_004_select_any_topics_exaccount_access(self):
        """
        DESCRIPTION: Select any Topics, Ex.Account Access
        EXPECTED: Selected topic's subcategory options are displayed
        """
        pass

    def test_005_select_any_option_from_the_subcategory_list(self):
        """
        DESCRIPTION: Select any option from the subcategory list
        EXPECTED: "Yes" and "No" buttons are displayed
        """
        pass

    def test_006_click_on_yes_button(self):
        """
        DESCRIPTION: Click on Yes button
        EXPECTED: My Account Details page is opened.
        EXPECTED: Live chat
        EXPECTED: Email
        EXPECTED: Visit our Help pages
        EXPECTED: Verify your details are displayed
        """
        pass

    def test_007_tap_on_live_chat_tab(self):
        """
        DESCRIPTION: Tap on 'Live chat' tab
        EXPECTED: User is navigated to "Live Chat" Page
        EXPECTED: Header with "Live Chat", minimise and close button are available
        EXPECTED: "You're one step away from talking to one of our experts, they'll be with you shortly." message is displayed.(if applicable)
        """
        pass

    def test_008_live_chat_is_active(self):
        """
        DESCRIPTION: Live chat is active
        EXPECTED: Wait until "Welcome 'username' to Coral Chat!" is displayed
        """
        pass

    def test_009_click_on_close_button(self):
        """
        DESCRIPTION: Click on Close Button
        EXPECTED: "You are about to terminate this Live Help. Are you sure you got the answer to your question?" message is displayed.
        EXPECTED: "Cancel" and "Close Chat" button are displayed
        """
        pass

    def test_010_tap_on_close_chat_button(self):
        """
        DESCRIPTION: Tap on Close Chat Button
        EXPECTED: User is on My Account Details Page
        """
        pass
