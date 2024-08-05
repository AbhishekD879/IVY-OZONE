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
class Test_C28839_Verify_Race_time_carousel__Section_Display(Common):
    """
    TR_ID: C28839
    NAME: Verify Race time carousel / Section Display
    DESCRIPTION: This test case verifies displaying of event off times
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-37132 Horse Racing / Greyhound : Header Redesign - Race Time Status [EDP]
    DESCRIPTION: BMA-10747 V2 - Horse Racing Events Details Page - Meeting Event Times
    DESCRIPTION: Applies to mobile, tablet & desktop
    PRECONDITIONS: To get data (event start time) about events use the following link:
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id =19
    PRECONDITIONS: 2) To get all 'Events' for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: *YYYY - a **comma-separated** values of class ID's (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'typeName' **to see event type (race meeting name)
    PRECONDITIONS: **'name'** on event level to see event name and local time
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_from_the_race_landing_page_tap_on_event_off(self):
        """
        DESCRIPTION: From the <Race> landing page tap on event off
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_section_where_event_off_times_tabs_are_displayed(self):
        """
        DESCRIPTION: Verify section where event off times tabs are displayed
        EXPECTED: Event off time tab is located under sub-header
        """
        pass

    def test_005_check_event_off_times_carousel(self):
        """
        DESCRIPTION: Check event off times carousel
        EXPECTED: * Event off times are displayed
        EXPECTED: * Event off times belong to the selected race meeting according to the Site Server response (see '**typeName' **attribute)
        EXPECTED: * Race meeting name 'typeName' is displayed (first 4 letters) under event off time (applied only for events from Next Races on Mobile/Tablets)
        """
        pass

    def test_006_verify_event_off_time_correctness_on_carousel(self):
        """
        DESCRIPTION: Verify event off time correctness on carousel
        EXPECTED: Event off time corresponds to the race local time
        """
        pass

    def test_007_verify_event_off_times_order(self):
        """
        DESCRIPTION: Verify event off times order
        EXPECTED: Events are displayed chronologically from left to right
        """
        pass

    def test_008_swipe_across_the_page_to_see_other_events(self):
        """
        DESCRIPTION: Swipe across the page to see other events
        EXPECTED: Scrolling (horizontally) allows user to see all event off times tabs for selected event type
        """
        pass

    def test_009_verify_current_selected_event(self):
        """
        DESCRIPTION: Verify current selected event
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Bet Filter link and icon are displayed in the header
        EXPECTED: * Meeting selector link and icon are displayed in the sub-header
        EXPECTED: * Event time / name corresponds to the SS response (see attributes **'name'**)
        EXPECTED: * Event off time tab is highlighted
        EXPECTED: * Event off time is in bold if priceTypeCodes="LP" attribute is present only for 'Win or Each way' market
        EXPECTED: **For desktop:**
        EXPECTED: * Bet Filter link and icon are displayed to the left of the 'Meetings' selector
        EXPECTED: * Meeting selector is displayed in the header with 'up'&'down' arrows
        EXPECTED: * Event breadcrumbs is displayed under event off times tabs;
        EXPECTED: * Event time / name corresponds to the SS response (see attributes **'name'**)
        EXPECTED: * Event off time tab is highlighted
        EXPECTED: * Event name is in bold if priceTypeCodes="LP" attribute is present only for 'Win or Each way' market
        """
        pass

    def test_010_tap_event_off_time_tab_where_event_is_not_started_yet(self):
        """
        DESCRIPTION: Tap event off time tab where event is NOT started yet
        EXPECTED: User is redirected to the selected event details page
        """
        pass

    def test_011_tap_event_off_time_tab_where_event_has_been_resulted(self):
        """
        DESCRIPTION: Tap event off time tab where event has been resulted
        EXPECTED: * Result icon is displayed next to the event off tab time
        EXPECTED: * User is redirected to the <Race> results page (if results are available) for that event
        """
        pass

    def test_012_change_race_meeting_using_race_selector(self):
        """
        DESCRIPTION: Change Race Meeting using race selector
        EXPECTED: User is redirected to the first available event landing page for selected race meeting
        """
        pass
