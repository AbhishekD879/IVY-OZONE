import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28473_Verify_Sport_In_Play_Event_Details_Page(Common):
    """
    TR_ID: C28473
    NAME: Verify <Sport> In-Play Event Details Page
    DESCRIPTION: This test case verifies <Sport> Event Details Page only for in-play events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. Event is **In-Play **(live) when:
    PRECONDITIONS: *   **drilldownTagNames="EVFLAG_BL" **(on the Event level)** **
    PRECONDITIONS: *   AND **isMarketBetInRun="true" **(on the any Market level)
    PRECONDITIONS: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_clicktap_onevent_name_in_the_event_card(self):
        """
        DESCRIPTION: Click/Tap on Event name in the event card
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page near label
        EXPECTED: **For desktop view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page, on the left side from Event name
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Event name matches with event name on the event section we navigated from
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the 'Back' button
        EXPECTED: **For desktop view:**
        EXPECTED: * It is displayed in the same line as 'Back' button, next to it
        EXPECTED: * Long names are truncated
        """
        pass

    def test_006_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: *   Event start date corresponds to **startTime** attribute
        EXPECTED: *   Event start time is shown in "<name of the day>, DD-MMM-YY. 24 hours HH:MM," format (e.g. "14:00 or 05:00)
        EXPECTED: *   Event start date/time matches with date/time on the event section we navigated from
        EXPECTED: *   Match time is shown instead of Event Start Time if available
        EXPECTED: It is displayed before Event Start Time
        """
        pass

    def test_007_verify_live_label_or_score(self):
        """
        DESCRIPTION: Verify 'LIVE' label or Score
        EXPECTED: 'LIVE'/Score is displayed if event is live now:
        EXPECTED: 1.  rawIsOffCode="Y"
        EXPECTED: 2.  rawIsOffCode="-" AND isStarted="true"
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed next to the Event Start Time
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed before Event Start Time
        """
        pass

    def test_008_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if drilldownTagNames attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        EXPECTED: EVFLAG_BL
        """
        pass

    def test_009_verify_market_tabs(self):
        """
        DESCRIPTION: Verify Market tabs
        EXPECTED: * They are displayed below the event details
        EXPECTED: * It is possible to navigate between all market tabs
        EXPECTED: * Order of market tabs is the same as in EDP-Markets response from CMS
        EXPECTED: * Collection with 'lastItem: true' is displayed the last one
        EXPECTED: * In case some collection is not added in CMS in is displayed before collection with 'lastItem: true' value
        EXPECTED: * In case there are several not added to CMS collections they are displayed before collection with 'lastItem: true' value, displayed in the order they are received
        """
        pass

    def test_010_verify_markets_filtering_within_in_play_event_details_page_for_all_available_collections_on_event_details_page(self):
        """
        DESCRIPTION: Verify Markets filtering within In-Play Event Details Page for all available Collections on Event Details Page
        EXPECTED: Only Markets with attribute **isMarketBetInRun="true"** on the market level are displayed
        """
        pass

    def test_011_verify_long_names_of_selections_for_markets_which_have_list_view_of_selections(self):
        """
        DESCRIPTION: Verify long names of selections for Markets, which have list view of selections
        EXPECTED: * Long names of selections are NOT TRUNCATED
        EXPECTED: * Long names of selections are wrapped into lines
        """
        pass

    def test_012_make_sure_you_can_get_to_the_bet_in_play_event_details_page_by_tapping___sporticon_from_the_sports_menu_ribbon_mobileleft_memu_desktop___event_name___sporticon_from_the_sports_menu_ribbon_mobileleft_memu_desktop___outrights_tab___event_name___liveicon_from_the_sports_menu_ribbon___event_name___featured_tab___event_name_if_live_event_is_available___in_play_tab___event_name(self):
        """
        DESCRIPTION: Make sure you can get to the Bet-In-Play Event Details page by tapping:
        DESCRIPTION: *   '<Sport>' icon from the Sports Menu Ribbon (Mobile)/Left Memu (Desktop) -> Event name
        DESCRIPTION: *   '<Sport>' icon from the Sports Menu Ribbon (Mobile)/Left Memu (Desktop) -> 'Outrights' tab -> Event name
        DESCRIPTION: *   'Live' icon from the Sports Menu Ribbon -> Event name
        DESCRIPTION: *   Featured tab -> Event name (if live event is available)
        DESCRIPTION: *   In-Play tab -> Event name
        EXPECTED: 
        """
        pass
