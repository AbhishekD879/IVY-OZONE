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
class Test_C1232375_Tracking_of_click_on_the_Next_Race_View_Full_Race_Card_link(Common):
    """
    TR_ID: C1232375
    NAME: Tracking of click on the Next Race "View Full Race Card" link
    DESCRIPTION: This test case verifies GA tracking of "View Full Race Card" link clicks
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_scroll_till_next_races_module_click_on_view_full_race_card_linktype_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Scroll till Next Races module. Click on "View Full Race Card" link.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'full race card'
        EXPECTED: })
        """
        pass
