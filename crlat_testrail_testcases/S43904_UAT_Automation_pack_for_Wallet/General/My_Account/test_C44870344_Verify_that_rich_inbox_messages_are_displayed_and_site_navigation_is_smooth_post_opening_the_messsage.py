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
class Test_C44870344_Verify_that_rich_inbox_messages_are_displayed_and_site_navigation_is_smooth_post_opening_the_messsage(Common):
    """
    TR_ID: C44870344
    NAME: Verify that rich inbox messages are displayed and site navigation is smooth post opening the messsage.
    DESCRIPTION: Verify;
    DESCRIPTION: 1. Display of site including Rich Inbox message
    DESCRIPTION: 2. Navigation to sports pages post opening message
    PRECONDITIONS: 1.Register a new user so that they will have a message in inbox.
    PRECONDITIONS: 2.User having rich inbox messages is logged in the application.
    PRECONDITIONS: 3.Message count is displayed on the header next to Balance on Desktop. On mobile the number (message count) is displayed under Right hand menu.
    """
    keep_browser_open = True

    def test_001_navigate_to_right_menumy_account_menu_and_click_on_messages_verify(self):
        """
        DESCRIPTION: Navigate to Right menu/My Account menu and click on Messages. Verify.
        EXPECTED: Unread rich inbox message count is displayed.
        """
        pass

    def test_002_click_on_the_message_and_verify(self):
        """
        DESCRIPTION: Click on the message and verify.
        EXPECTED: On Desktop & Tablet, the full message is opened and displayed.
        EXPECTED: On mobile subject is displayed. On clicking the subject, full message is displayed.
        """
        pass

    def test_003_click_on_close_x_button_verify_the_layout(self):
        """
        DESCRIPTION: Click on close (X) button. Verify the layout.
        EXPECTED: The message box is closed and the user is taken to the Homepage.
        """
        pass

    def test_004_click_on_closex_button_navigate_to_the_following_pages_and__verify_if_the_navigation_is_taking_you_to_the_correct_pages1_home_page2_sport_landing_pages_for_few_sports___football_tennis_horses_greyhounds_virtuals_inplay_etc(self):
        """
        DESCRIPTION: Click on close(X) button. Navigate to the following pages and  Verify if the navigation is taking you to the correct pages.
        DESCRIPTION: 1. Home page
        DESCRIPTION: 2. Sport landing pages for few sports - Football, tennis, horses, greyhounds, virtuals, inplay etc
        EXPECTED: 1. The layout for all the pages is as correct/as per design.
        EXPECTED: 2. The navigation for all the pages is smooth.
        EXPECTED: 3. User is navigated to respective pages when clicked.
        """
        pass
