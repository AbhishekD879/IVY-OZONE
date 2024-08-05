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
class Test_C1232389_Tracking_of_Tweet_Now_button_clicks(Common):
    """
    TR_ID: C1232389
    NAME: Tracking of “Tweet Now” button clicks
    DESCRIPTION: This test case verifies GA tracking of “Tweet Now” button clicks.
    PRECONDITIONS: YourCall page is opened. (HR Landing page> YourCall tab)
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_on_yourcall_page_page_tap_the_tweet_now_button(self):
        """
        DESCRIPTION: On YourCall page page, tap the “Tweet Now” button.
        EXPECTED: ''Tweet Now'' button opens the twitter website(configured in CMS-> Your Call-> YOUR CALL STATIC BLOCKS  YOURCALL-RACING).
        """
        pass

    def test_002_on_the_oxygen_browser_tab_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: On the Oxygen browser tab type in browser console "dataLayer" and press "Enter".
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'tweet now',
        EXPECTED: 'eventLabel' : 'horse racing'
        EXPECTED: })
        """
        pass
