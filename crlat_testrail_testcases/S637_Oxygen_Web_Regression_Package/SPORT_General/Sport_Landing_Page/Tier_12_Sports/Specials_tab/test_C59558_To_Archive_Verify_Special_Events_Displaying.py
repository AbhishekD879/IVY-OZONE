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
class Test_C59558_To_Archive_Verify_Special_Events_Displaying(Common):
    """
    TR_ID: C59558
    NAME: [To Archive] Verify Special Events Displaying
    DESCRIPTION: This test case verifies data which is displayed on Specials tab
    DESCRIPTION: AUTOTEST [C527861]
    PRECONDITIONS: 1. In order to get a list of special events use link:
    PRECONDITIONS: {domain}/openbet-ssviewer/Drilldown/2.19/EventToOutcomeForClass/{classIds}?simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.suspendAtTime:greaterThan:ZZZZ-YY-XXT10:34:30.000Z&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_SP&prune=event&prune=market
    PRECONDITIONS: where, ZZZZ-YY-XX - is a current date
    PRECONDITIONS: Note, event is set as special when typeFlagCodes = MKTFLAG_SP
    PRECONDITIONS: Where domain is:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
    PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
    PRECONDITIONS: 2. Make sure special events are available
    PRECONDITIONS: 3. Make sure there are no events from typeId = 2652
    PRECONDITIONS: 4. In order to configure special events go to the Open Bet TI, find the event, open market and tick 'Special' flag
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Oxygen app is loaded
        """
        pass

    def test_002_for_mobiletabletnavigate_to_football_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_football_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Football' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Football' Landing page from the 'Left Navigation' menu
        EXPECTED: 'Football' sport page is opened
        """
        pass

    def test_003_clicktap_specials_tab(self):
        """
        DESCRIPTION: Click/Tap 'Specials' tab
        EXPECTED: Specials tab with events available is shown
        """
        pass

    def test_004_open_special_module(self):
        """
        DESCRIPTION: Open special module
        EXPECTED: Special events which are related to the selected type are shown
        """
        pass

    def test_005_check_event_data(self):
        """
        DESCRIPTION: Check event data
        EXPECTED: Only events which have the next attributes will be shown:
        EXPECTED: * drilldownTagNames = EVFLAG_SP
        EXPECTED: * typeFlagCodes=SP
        """
        pass

    def test_006_check_events_ordering(self):
        """
        DESCRIPTION: Check events ordering
        EXPECTED: Events within one competition are ordered by start date and time (see startTime attribute from the Site Server response)
        EXPECTED: Note, start date and time are NOT displayed for those events
        """
        pass

    def test_007_check_special_event_displaying_is_event_contains_only_one_selection_in_the_special_market(self):
        """
        DESCRIPTION: Check special event displaying is event contains only one selection in the special market
        EXPECTED: Selection name and price/odds button is shown
        """
        pass

    def test_008_clicktap_selection_name(self):
        """
        DESCRIPTION: Click/Tap selection name
        EXPECTED: Event details page is opened
        """
        pass

    def test_009_check_special_event_displaying_when_event_contains_more_than_one_selection__within_market(self):
        """
        DESCRIPTION: Check special event displaying when event contains more than one selection  within market
        EXPECTED: * Only event name is shown
        EXPECTED: * When event name is tapped - event details page is opened
        """
        pass

    def test_010_check_events_removal_from_the_front_end(self):
        """
        DESCRIPTION: Check events removal from the front end
        EXPECTED: Football Special Event disappear only after receiving undisplayed=true from the SS
        """
        pass
