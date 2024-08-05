import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9770894_Tracking_of_viewing_Tier_III_Sport_upcoming_event(Common):
    """
    TR_ID: C9770894
    NAME: Tracking of viewing Tier III Sport upcoming event
    DESCRIPTION: This test case verifies the GA tracking of viewing upcoming event on sport landing page of Ties III type
    PRECONDITIONS: 1. Sports Page > Sports Categories > <any sport> is enabled in CMS
    PRECONDITIONS: 2. User is on <sport> landing page: Single view page
    PRECONDITIONS: All sports that are tier I and II are listed here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True

    def test_001_click_on_any_event_from_upcoming_module(self):
        """
        DESCRIPTION: Click on any event from Upcoming module
        EXPECTED: User is redirected to EDP
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event': 'trackEvent', 'eventCategory': 'upcoming module ', 'eventAction': '&lt;&lt; LOCATION &gt;&gt;', 'eventLabel': 'view event', 'eventName': '&lt;&lt; EVENT NAME &gt;&gt;', 'eventID': '&lt;&lt; EVENT ID &gt;&gt;' }
        """
        pass
