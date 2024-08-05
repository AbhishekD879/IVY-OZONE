import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
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
        pass

    def test_002_close_overlayopen_user_menu_and_click_messages(self):
        """
        DESCRIPTION: Close overlay.
        DESCRIPTION: Open User menu and click 'Messages'
        EXPECTED: * Overlay opens with 'My Inbox' title and Close (X) button.
        EXPECTED: * 'You have no messages!' message displayed is user has no messages
        EXPECTED: * List of messages displayed if user has any.
        """
        pass
