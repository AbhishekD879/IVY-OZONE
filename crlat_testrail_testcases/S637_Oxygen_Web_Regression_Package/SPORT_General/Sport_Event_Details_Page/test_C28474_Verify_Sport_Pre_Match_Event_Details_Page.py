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
class Test_C28474_Verify_Sport_Pre_Match_Event_Details_Page(Common):
    """
    TR_ID: C28474
    NAME: Verify <Sport> Pre-Match Event Details Page
    DESCRIPTION: This test case verifies <Sport> Event Details Page
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
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

    def test_003_clicktap_onevent_name_on_the_event_card(self):
        """
        DESCRIPTION: Click/Tap on Event name on the event card
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify back button
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page near label
        EXPECTED: **For desktop view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page, on the left side from Event name
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
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
        DESCRIPTION: Verify event start date/time
        EXPECTED: *   Event start date corresponds to **startTime** attribute
        EXPECTED: *   Event start time is shown in "<name of the day>, DD-MMM-YY. 24 hours HH:MM" format (e.g. "14:00 or 05:00,)
        EXPECTED: *   Event start date/time matches with date/time on the event section we navigated from
        EXPECTED: *   Match time is shown instead of Event Start Time if available
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the event name
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed in the same line as Event name, on the right side
        """
        pass

    def test_007_verify_market_tabs(self):
        """
        DESCRIPTION: Verify market tabs
        EXPECTED: * They are displayed below the event details
        EXPECTED: * It is possible to navigate between all market tabs
        EXPECTED: * Order of market tabs is the same as in EDP-Markets response from CMS
        EXPECTED: * Collection with 'lastItem: true' is displayed the last one
        EXPECTED: * In case some collection is not added in CMS in is displayed before collection with 'lastItem: true' value
        EXPECTED: * In case there are several not added to CMS collections they are displayed before collection with 'lastItem: true' value, displayed in the order they are received
        """
        pass

    def test_008_verify_long_names_of_selections_for_markets_which_have_list_view_of_selections(self):
        """
        DESCRIPTION: Verify long names of selections for Markets, which have list view of selections
        EXPECTED: * Long names of selections are NOT TRUNCATED
        EXPECTED: * Long names of selections are wrapped into lines
        """
        pass

    def test_009_make_sure_you_can_get_to_the_pre_match_event_details_page_by_tapping___sporticon_from_the_sports_menu_ribbon_mobileleft_memu_desktop___event_name___featured_tab___event_name(self):
        """
        DESCRIPTION: Make sure you can get to the Pre-Match Event Details page by tapping:
        DESCRIPTION: *   '<Sport>' icon from the Sports Menu Ribbon (Mobile)/Left Memu (Desktop) -> Event name
        DESCRIPTION: *   Featured tab -> Event name
        EXPECTED: 
        """
        pass
