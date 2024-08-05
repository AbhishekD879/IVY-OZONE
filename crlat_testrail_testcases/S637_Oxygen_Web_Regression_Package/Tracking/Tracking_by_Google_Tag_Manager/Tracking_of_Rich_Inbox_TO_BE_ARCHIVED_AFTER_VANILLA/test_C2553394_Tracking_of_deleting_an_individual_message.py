import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2553394_Tracking_of_deleting_an_individual_message(Common):
    """
    TR_ID: C2553394
    NAME: Tracking of deleting an individual message
    DESCRIPTION: This test case verifies tracking when user taps on "Delete" icon
    PRECONDITIONS: - To see what CMS is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - "Rich Inbox" menu item should be configured and active in CMS > Menus > Right Menus
    PRECONDITIONS: - "Rich Inbox" feature toggle should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should have a user with messages
    PRECONDITIONS: - You should be logged in
    """
    keep_browser_open = True

    def test_001___open_browsers_console__tap_on_a_header__rich_inbox_menu_open_any_message_and_delete_it(self):
        """
        DESCRIPTION: - Open browser's console
        DESCRIPTION: - Tap on a header > "Rich Inbox" menu, open any message and delete it
        EXPECTED: Message is deleted
        """
        pass

    def test_002_in_browsers_console_type_datalayer(self):
        """
        DESCRIPTION: In browser's console type "dataLayer"
        EXPECTED: There is a record that user did a tap on "Messages" menu:
        EXPECTED: dataLayer.push{
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'inbox - sports',
        EXPECTED: 'eventAction' : 'delete message',
        EXPECTED: 'eventLabel' : '<< MESSAGE ID/NAME >>'
        EXPECTED: }
        """
        pass
