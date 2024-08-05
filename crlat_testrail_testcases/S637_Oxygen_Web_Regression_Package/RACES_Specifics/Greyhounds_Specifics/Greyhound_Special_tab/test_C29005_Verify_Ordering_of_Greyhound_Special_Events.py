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
class Test_C29005_Verify_Ordering_of_Greyhound_Special_Events(Common):
    """
    TR_ID: C29005
    NAME: Verify Ordering of Greyhound Special Events
    DESCRIPTION: This test case verifies 'Greyhound special' events ordering
    PRECONDITIONS: To retrieve an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = 201 for Greyhound Specials class
    PRECONDITIONS: See attribute:
    PRECONDITIONS: **'name' **- on event level to see event`s start time
    PRECONDITIONS: **'startTime'** to see event start time
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
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
        EXPECTED: *   Greyhounds landing page is opened
        EXPECTED: *   The 'Today' tab is chosen by default
        EXPECTED: *   By Meeting' sorting type is selected
        """
        pass

    def test_003_verify_special_event_types_ordering(self):
        """
        DESCRIPTION: Verify special event types ordering
        EXPECTED: All special event types are displayed in alphabetical A-Z order
        """
        pass

    def test_004_go_to_the_event_section(self):
        """
        DESCRIPTION: Go to the Event section
        EXPECTED: 
        """
        pass

    def test_005_verify_events_ordering_within_each_type(self):
        """
        DESCRIPTION: Verify events ordering within each type
        EXPECTED: *   Events are ordered by** 'startTime'** attribute in the fist instance
        EXPECTED: *   Events are sorted alphabetically **by name** in ascending order if start times are the same
        """
        pass
