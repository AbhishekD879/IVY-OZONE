import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1108081_Verify_Next_Races_Header_Race_Time(Common):
    """
    TR_ID: C1108081
    NAME: Verify 'Next Races' Header & Race Time
    DESCRIPTION: This test case if for checking the correctness of 'Next Races' module header and race time.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: AUTOTEST [C10791965]
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To control Events displaying in the Next Races Widget on the Horse Racing page, go to **CMS**  -> Tap '**System-configuration**' -> **NEXTRACES**
    PRECONDITIONS: To load CMS use the next link: CMS_ENDPOINT/keystone/structure where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2) To retrieve all events by class id included in the module use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: 3) Parameter typeName defines 'Race Meetings' name
    PRECONDITIONS: Parameter 'startTime' defines event start time (note, this is not a race local time)
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * <Horse Racing> landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' module is displayed
        """
        pass

    def test_002_verify_next_races_accordion_header(self):
        """
        DESCRIPTION: Verify 'Next Races' accordion header
        EXPECTED: * The title of the Header is 'Next Races' (*\***|Header is CMS controlled & internationalised\***|)*
        EXPECTED: * The title is displayed on the left side of the accordion
        """
        pass

    def test_003_verify_the_next_races_accordion_collapseexpand_state(self):
        """
        DESCRIPTION: Verify the 'Next Races' accordion collapse/expand state
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 1. From default state 'expanded', Next Races’ module should collapse when tapping ( - ) or any other area of the accordion header
        EXPECTED: 2. 'Next Races’ module should expand back when tapping ( + ) or any other area of the accordion header
        EXPECTED: Note: this is for Coral only, on Ladbrokes there is 'Next Races' tab
        EXPECTED: **For Desktop:**
        EXPECTED: * From default state 'expanded', Next Races’ module collapses when tapping the arrow-down symbol or any other area of the accordion header
        EXPECTED: * 'Next  Races’ module expands back when tapping the arrow-up symbol or any other area of the accordion header
        EXPECTED: Note: The '^' arrow symbol is displayed on the right side of the accordion
        """
        pass

    def test_004_verify_sub_header(self):
        """
        DESCRIPTION: Verify sub-header
        EXPECTED: * Race sub-header is shown in next format** 'HH:MM EventName' [Example: "1:40 FAKENHAM"]
        EXPECTED: * Cash Out icon is shown on the right if the event has cashoutAvail="Y in SS response
        EXPECTED: * Text IS NOT clickable
        """
        pass

    def test_005_verify_each_way_terms_in_sub_header(self):
        """
        DESCRIPTION: Verify each way terms in sub header
        EXPECTED: Each way terms are NOT shown even if  **isEachWayAvailable='true'**
        """
        pass

    def test_006_verify_event_time_and_name_correctness(self):
        """
        DESCRIPTION: Verify event time and name correctness
        EXPECTED: Event time and name correspond to the **'name'** attribute from the Site Server response
        """
        pass

    def test_007_for_desktopgo_to_the_desktop_homepage___check_next_races_carousel_under_the_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' carousel under the In-Play widget
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' carousel is shown
        """
        pass

    def test_008_for_desktoprepeat_steps__3___6(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 3 - 6
        EXPECTED: --
        """
        pass
