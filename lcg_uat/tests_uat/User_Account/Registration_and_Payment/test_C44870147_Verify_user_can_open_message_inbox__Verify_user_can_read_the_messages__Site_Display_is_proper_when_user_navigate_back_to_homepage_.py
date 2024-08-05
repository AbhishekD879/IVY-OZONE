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
class Test_C44870147_Verify_user_can_open_message_inbox__Verify_user_can_read_the_messages__Site_Display_is_proper_when_user_navigate_back_to_homepage_(Common):
    """
    TR_ID: C44870147
    NAME: "Verify user can open message inbox - Verify user can read the messages - Site Display is proper when user navigate back to homepage  "
    DESCRIPTION: 
    PRECONDITIONS: "Rich Inbox" module should be created and active in CMS > Menus > Right Menus
    PRECONDITIONS: "Rich Inbox" feature toggle should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: Your user should have at least 1 message received
    PRECONDITIONS: You should be logged in
    """
    keep_browser_open = True

    def test_001_mobile_and_tablettap_on_a_header(self):
        """
        DESCRIPTION: Mobile and tablet:
        DESCRIPTION: Tap on a header
        EXPECTED: Right menu is opened and "Rich Inbox" menu is present
        """
        pass

    def test_002_mobile_and_tablettap_on_a_messages_menu(self):
        """
        DESCRIPTION: Mobile and tablet:
        DESCRIPTION: Tap on a "Messages" menu
        EXPECTED: Mobile:
        EXPECTED: - "Messages" page with a list of messages is opened
        EXPECTED: Tablet:
        EXPECTED: - "Messages" page divided into 2 columns is loaded
        EXPECTED: - Left column contains list of messages
        EXPECTED: - Right columns contains message details
        """
        pass

    def test_003_mobile_and_tablettap_on_any_message(self):
        """
        DESCRIPTION: Mobile and tablet:
        DESCRIPTION: Tap on any message
        EXPECTED: Mobile:
        EXPECTED: Message details page is opened
        EXPECTED: Tablet:
        EXPECTED: Message details is opened in a right column
        """
        pass

    def test_004_mobile_and_tablettap_x_button(self):
        """
        DESCRIPTION: Mobile and tablet:
        DESCRIPTION: Tap "X" button
        EXPECTED: "Messages" overlay is closed
        """
        pass

    def test_005_mobile_only__tap_on_a_header__rich_inbox_menu_and_open_any_message__tap_back_button(self):
        """
        DESCRIPTION: Mobile only:
        DESCRIPTION: - Tap on a header > "Rich Inbox" menu and open any message
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to "Messages" page with a list of messages
        """
        pass

    def test_006_mobile_onlytap_x_button(self):
        """
        DESCRIPTION: Mobile only:
        DESCRIPTION: Tap "X" button
        EXPECTED: "Messages" overlay is closed
        """
        pass
