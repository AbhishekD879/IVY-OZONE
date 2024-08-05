import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.uat
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870344_Verify_that_rich_inbox_messages_are_displayed_and_site_navigation_is_smooth_post_opening_the_messsage(Common):
    """
    TR_ID: C44870344
    NAME: Verify that rich inbox messages are displayed and site navigation is smooth post opening the messsage.
    DESCRIPTION: Verify;
    DESCRIPTION: 1. Display of site including Rich Inbox message
    DESCRIPTION: 2. Navigation to sports pages post opening message
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1.Register a new user so that they will have a message in inbox.
        PRECONDITIONS: 2.User having rich inbox messages is logged in the application.
        PRECONDITIONS: 3.Message count is displayed on the header next to Balance on Desktop. On mobile the number (message count) is displayed under Right hand menu.
        """
        # Registering user to get new messages on the both devices
        user = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user)
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.user_panel.my_inbox_button.is_displayed(),
                            msg='"Inbox button" is not displayed')
            self.assertTrue(self.site.messages.counter, msg='Message counter is not displayed')

    def test_001_navigate_to_right_menumy_account_menu_and_click_on_messages_verify(self):
        """
        DESCRIPTION: Navigate to Right menu/My Account menu and click on Messages. Verify.
        EXPECTED: Unread rich inbox message count is displayed.
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Right menu is not opened')
        self.assertTrue(self.site.messages.counter, msg='Message counter is not displayed')
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

    def test_002_click_on_the_message_and_verify(self):
        """
        DESCRIPTION: Click on the message and verify.
        EXPECTED: On Desktop & Tablet, the full message is opened and displayed.
        EXPECTED: On mobile subject is displayed. On clicking the subject, full message is displayed.
        """
        if self.device_type == 'mobile':
            self.site.wait_splash_to_hide(timeout=1)
            self.site.messages.message_expand.click()
        self.assertTrue(self.site.messages.message_details.is_displayed(), msg="Message is not displayed")

    def test_003_click_on_close_x_button_verify_the_layout(self):
        """
        DESCRIPTION: Click on close (X) button. Verify the layout.
        EXPECTED: The message box is closed and the user is taken to the Homepage.
        """
        if self.device_type == 'mobile':
            self.assertTrue(self.site.messages.back_button.is_displayed(),
                            msg='"back button of message body" is not displayed')
            self.site.messages.back_button.click()
            self.assertTrue(self.site.messages.back_button.is_displayed(),
                            msg='"back button of message inbox" is not displayed')
            self.site.messages.back_button.click()
            self.site.right_menu.close_icon.click()
        else:
            self.assertTrue(self.site.messages.close_button.is_displayed(), msg='"close button of message dialog box" is not displayed')
            self.site.messages.close_button.click()
        self.site.wait_content_state('Homepage')

    def test_004_click_on_closex_button_navigate_to_the_following_pages_and__verify_if_the_navigation_is_taking_you_to_the_correct_pages1_home_page2_sport_landing_pages_for_few_sports___football_tennis_horses_greyhounds_virtuals_inplay_etc(self):
        """
        DESCRIPTION: Click on close(X) button. Navigate to the following pages and  Verify if the navigation is taking you to the correct pages.
        DESCRIPTION: 1. Home page
        DESCRIPTION: 2. Sport landing pages for few sports - Football, tennis, horses, greyhounds, virtuals, inplay etc
        EXPECTED: 1. The layout for all the pages is as correct/as per design.
        EXPECTED: 2. The navigation for all the pages is smooth.
        EXPECTED: 3. User is navigated to respective pages when clicked.
        """
        if self.device_type == 'mobile':
            home_tabs = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            home_tabs = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(home_tabs, msg='"Header Menu" item dictionary is empty')

        expected_sports = [vec.siteserve.FOOTBALL_TAB.upper(), vec.sb.HORSERACING.upper(), vec.siteserve.IN_PLAY_TAB, vec.siteserve.TENNIS_TAB.upper()]
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            expected_sports = [vec.siteserve.FOOTBALL_TAB, vec.sb.HORSERACING, vec.siteserve.IN_PLAY_TAB.capitalize(), vec.siteserve.TENNIS_TAB]

        for sport_name in home_tabs:
            if self.device_type == 'mobile':
                home_tabs = self.site.home.menu_carousel.items_as_ordered_dict
            for each_sport in expected_sports:
                if sport_name == each_sport:
                    home_tabs[sport_name].click()
                    page_title = self.site.sports_page.header_line.page_title
                    self.assertTrue(page_title.is_displayed(),
                                    msg=f'Page title: "{page_title.text}" is not displayed')
                    if self.brand == 'bma':
                        self.assertTrue(self.site.sports_page.is_back_button_displayed(),
                                        msg='"back button" is not present in navigated page')
                        self.site.sports_page.header_line.back_button.click()
                    else:
                        self.site.back_button.click()
                    self.site.wait_content_state('homepage', timeout=5)
