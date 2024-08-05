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
class Test_C2987520_Tracking_of_viewing_Tier_I_II_Sports_upcoming_event(Common):
    """
    TR_ID: C2987520
    NAME: Tracking of viewing Tier I/II Sports upcoming event
    DESCRIPTION: This test case verifies the GA tracking of viewing upcoming event on sport Matches tab (sport is Tier I or II type)
    PRECONDITIONS: 1. Sports Page > Sports Categories > <any sport> is enabled in CMS
    PRECONDITIONS: 2. User is on <sport> landing page: 'Matches' tab
    PRECONDITIONS: All sports that are tier I and II are listed here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True

    def test_001_click_on_any_upcoming_event(self):
        """
        DESCRIPTION: Click on any upcoming event
        EXPECTED: User is redirected to EDP
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: After user views the event the following tracking fires:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event': 'trackEvent', 'eventCategory': 'upcoming module ', 'eventAction': '<< LOCATION >>', 'eventLabel': 'view event', 'eventName': '<< EVENT NAME >>', 'eventID': '<< EVENT ID >>' }
        """
        pass
