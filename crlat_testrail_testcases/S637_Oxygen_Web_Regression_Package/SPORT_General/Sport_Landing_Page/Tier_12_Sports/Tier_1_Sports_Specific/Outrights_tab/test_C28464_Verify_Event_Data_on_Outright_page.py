import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28464_Verify_Event_Data_on_Outright_page(Common):
    """
    TR_ID: C28464
    NAME: Verify Event Data on Outright page
    DESCRIPTION: This test case verifies event data on Outright page
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: for Football Sport only, Outright' tab is removed from the module header into 'Competition Module Header' within 'Matches' tab
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_sport_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_sport_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the 'Left Navigation' menu
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED: 
        """
        pass

    def test_004_verify_outrights_event_card(self):
        """
        DESCRIPTION: Verify 'Outrights' Event card
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Time and Date is removed from the 'Outrights' Event card
        EXPECTED: *   'Show All' button is removed from the 'Outrights' Event card
        EXPECTED: *   If 'LIVE' label is available, it is displayed next to 'Outrights' Event Name
        """
        pass

    def test_005_clicktap_anywhere_whithin_outrights_event_card(self):
        """
        DESCRIPTION: Click/Tap anywhere whithin 'Outrights' Event card
        EXPECTED: 'Outright' Event details page is opened
        """
        pass

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * It is displayed below the Event name
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: * Event start date is shown in following format: ** HH:MM, ## MMM **
        EXPECTED: <HH:MM> is a 24 hour time range(i.e. 23:59)
        EXPECTED: <##> is the date integer value(i.e. 21, 31, 11)
        EXPECTED: <MMM> is the shortened name of the month(i.e. Mar, Apr, May)
        EXPECTED: **For Desktop:**
        EXPECTED: * It is displayed below in the right side of Sport Header
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: * Event start date is shown in** '<name of the day>, DD-MMM-YY. 12 hours AM/PM'** format
        """
        pass

    def test_007_verify_live_label(self):
        """
        DESCRIPTION: Verify 'LIVE' label
        EXPECTED: 'LIVE' label is shown if event is live now: rawIsOffCode="Y" OR rawIsOffCode="-" AND isStarted="true"
        """
        pass
