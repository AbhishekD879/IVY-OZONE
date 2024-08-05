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
class Test_C2553393_Tracking_of_taps_on_a_CTA(Common):
    """
    TR_ID: C2553393
    NAME: Tracking of taps on a CTA
    DESCRIPTION: This test case verifies tracking when user taps on a CTA from message details page
    PRECONDITIONS: - To see what CMS is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - "Rich Inbox" menu item should be configured and active in CMS > Menus > Right Menus
    PRECONDITIONS: - "Rich Inbox" feature toggle should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should have a user with messages and the message should have a CTA item (e.g. button)
    PRECONDITIONS: - You should be logged in
    """
    keep_browser_open = True

    def test_001___open_browsers_console__tap_on_a_header__rich_inbox_menu_open_any_message_and_tap_on_a_cta(self):
        """
        DESCRIPTION: - Open browser's console
        DESCRIPTION: - Tap on a header > "Rich Inbox" menu, open any message and tap on a CTA
        EXPECTED: User is navigated to the URL configured for the CTA
        """
        pass

    def test_002_in_browsers_console_type_datalayer(self):
        """
        DESCRIPTION: In browser's console type "dataLayer"
        EXPECTED: There is a record that user did a tap on "Messages" menu:
        EXPECTED: dataLayer.push{
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'inbox - sports',
        EXPECTED: 'eventAction' : 'message cta',
        EXPECTED: 'eventLabel' : '<<CTA>>'
        EXPECTED: }
        """
        pass