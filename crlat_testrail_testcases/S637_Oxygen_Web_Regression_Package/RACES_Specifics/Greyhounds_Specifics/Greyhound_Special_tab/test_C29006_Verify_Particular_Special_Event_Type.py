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
class Test_C29006_Verify_Particular_Special_Event_Type(Common):
    """
    TR_ID: C29006
    NAME: Verify Particular Special Event Type
    DESCRIPTION: This test case verifies Particular event type for Greyhound Special Events (e.g. Winning Distances, Trap Challenges etc.)
    PRECONDITIONS: In order to get an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = 201 for Greyhound Specials class
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_laod_invictus(self):
        """
        DESCRIPTION: Laod Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' homepage is opened
        """
        pass

    def test_003_go_to_the_special_events_sections(self):
        """
        DESCRIPTION: Go to the Special Events sections
        EXPECTED: Special Event types are shown
        """
        pass

    def test_004_verify_events_within_one_event_type_section(self):
        """
        DESCRIPTION: Verify events within one event type section
        EXPECTED: All events which are related to the particular event type is shown
        EXPECTED: Each event is shown in a separate section
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name correspons to the** 'name' **attribute from the Site Server
        """
        pass

    def test_006_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: Event details page is opened
        """
        pass
