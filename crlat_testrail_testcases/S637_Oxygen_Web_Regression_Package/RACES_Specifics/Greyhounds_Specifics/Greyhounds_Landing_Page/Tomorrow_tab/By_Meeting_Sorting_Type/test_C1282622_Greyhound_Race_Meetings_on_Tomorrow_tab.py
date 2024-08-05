import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1282622_Greyhound_Race_Meetings_on_Tomorrow_tab(Common):
    """
    TR_ID: C1282622
    NAME: Greyhound Race Meetings on Tomorrow tab
    DESCRIPTION: This test case verifies Race Meetings displaying within Greyhound Race Grid on Tomorrow tab
    DESCRIPTION: New design (Ladbrokes Desktop): https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Classe IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XX - category id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get all 'Events' for the class ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY is a comma separated list of class ID's (e.g. 97 or 97, 98).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Parameter  **'typeName'**  defines 'Race Meetings' name
    PRECONDITIONS: Parameter **'startTime'** defines event start time (note, this is not a race local time)
    PRECONDITIONS: NOTE: Cashout icons removed for LADBROKES within BMA-39817
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Greyhound landing page -> 'TODAY'tab is selected by default
    PRECONDITIONS: Navigate to the 'TOMORROW' tab
    """
    keep_browser_open = True

    def test_001_check_order_of_race_meetings_inside_the_race_grid_section_eg_tomorrows_races(self):
        """
        DESCRIPTION: Check order of race meetings inside the race grid section (e.g. 'TOMORROWS RACES')
        EXPECTED: Race meetings are ordered in ascending alphabetical order (A-Z)
        """
        pass

    def test_002_verify_race_meeting_sections_content(self):
        """
        DESCRIPTION: Verify Race meeting sections content
        EXPECTED: * Race meeting header
        EXPECTED: * Row of events start time
        """
        pass

    def test_003_verify_race_meeting_header_line_content(self):
        """
        DESCRIPTION: Verify Race meeting header line content
        EXPECTED: * Race race meeting name on the left
        EXPECTED: * Each race meeting name corresponds to the '**typeName'** parameter from the Site Server response
        EXPECTED: * Race meeting name is NOT clickable
        EXPECTED: * Live Stream icon (if available) on the right
        """
        pass

    def test_004_only_coral_verify_cash_out_icon_displaying(self):
        """
        DESCRIPTION: Only Coral: Verify 'Cash Out' icon displaying
        EXPECTED: **FOR CORAL Only**
        EXPECTED: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        """
        pass

    def test_005_verify_live_stream_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' icon
        EXPECTED: * Stream icon is displayed (if available) on the right
        EXPECTED: * **FOR CORAL** Play icon for races with live stream (if available) on the right
        EXPECTED: * **FOR LADBROKES** WATCH icon for races with live stream (if available) on the right
        EXPECTED: * Stream icon is shown for event type where stream is applicable
        EXPECTED: * Stream icon is for informational purpose only
        """
        pass

    def test_006_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying
        EXPECTED: * Event off times are displayed horizontally across the page
        EXPECTED: * **FOR CORAL** Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        EXPECTED: * **FOR LADBROKES** ALL events off times are displayed in bold no matter if it is 'LP' or 'SP' prices
        EXPECTED: * Ladbrokes: Race Statuses displayed for started or resulted events:
        EXPECTED: Race Off - event has 'isOff=Yes'
        EXPECTED: Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: Resulted - event has 'isResulted=true' + 'isFinished=true'
        EXPECTED: * Coral: Signposting icons are displayed next to event off time (if available)
        EXPECTED: * Ladbrokes: Signposting icons are NOT displayed next to event off time
        """
        pass

    def test_007_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times
        EXPECTED: Event off times corresponds to the race local time from the **'name'** attribute from the Site Server
        """
        pass

    def test_008_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times
        EXPECTED: On **Mobile/Tablet** ability to scroll left and right is available via swiping
        EXPECTED: On **Desktop** Race meeting with too many event off times to be shown in one line has arrows which appear on hover to scroll horizontally.
        EXPECTED: Events off times are scrolled one by one after click arrows
        """
        pass

    def test_009_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time
        EXPECTED: Corresponding Event details page is opened
        """
        pass

    def test_010_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Greyhound Landing page is opened
        """
        pass
