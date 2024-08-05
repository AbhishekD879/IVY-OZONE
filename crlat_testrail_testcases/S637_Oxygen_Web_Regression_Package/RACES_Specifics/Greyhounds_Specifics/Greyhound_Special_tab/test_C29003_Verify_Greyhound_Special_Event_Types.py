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
class Test_C29003_Verify_Greyhound_Special_Event_Types(Common):
    """
    TR_ID: C29003
    NAME: Verify 'Greyhound Special' Event Types
    DESCRIPTION: This test case verifies which events are related to the 'Greyhound Special' events and how they should be displayed in the 'Invictus' application
    PRECONDITIONS: To retrieve an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **Class id** = 201 - Greyhound specails
    PRECONDITIONS: **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: **Greyhounds Specials present only for Today tab and only on 'By Meeting' sorting type**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load 'Invictus' application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        pass

    def test_004_verify_special_event_types(self):
        """
        DESCRIPTION: Verify special event types
        EXPECTED: All available special event types are shown
        EXPECTED: Special events are shown below the 'All Races' group
        """
        pass

    def test_005_verify_special_event_types_displaying(self):
        """
        DESCRIPTION: Verify special event types displaying
        EXPECTED: Special event sections are expanded by default
        EXPECTED: It is possible to collapse / expand section by tapping section header
        EXPECTED: Each section contains events withing it
        """
        pass

    def test_006_verify_section_headers(self):
        """
        DESCRIPTION: Verify section headers
        EXPECTED: The section headers correspond to **'typeName' **attributes on the Site Server
        """
        pass

    def test_007_verify_special_events_if_they_are_not_available_on_the_site_server(self):
        """
        DESCRIPTION: Verify special events if they are not available on the Site Server
        EXPECTED: If events for event type are not available -&gt; sections should not be shown at all
        """
        pass

    def test_008_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        pass
