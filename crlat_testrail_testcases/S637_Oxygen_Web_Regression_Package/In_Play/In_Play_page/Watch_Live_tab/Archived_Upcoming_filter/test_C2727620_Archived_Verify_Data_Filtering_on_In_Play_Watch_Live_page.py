import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C2727620_Archived_Verify_Data_Filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727620
    NAME: [Archived] Verify Data Filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies data filtering on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 3. Select 'Upcoming' switcher
    PRECONDITIONS: In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports Category ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: For each Class retrieve a list of Event IDs:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXX?simpleFilter=event.siteChannels:contains:M&simpleFilter=market.siteChannels:contains:M&simpleFilter=market.isMarketBetInRun&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_BL&simpleFilter=event.isNext24HourEvent&simpleFilter=event.isStarted:isFalse&existsFilter=event:simpleFilter:market.isDisplayed&existsFilter=event:simpleFilter:market.isMarketBetInRun&existsFilter=event:simpleFilter:market.isResulted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:YYYY-MM-DDTHH:MM:SSZ&translationLang=en
    PRECONDITIONS: *   XXX -  is a comma separated list of Class ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYYY-MM-DD HH:MM:SS - date/time when SS request is made (The time needs to be rounded to the nearest minute or 30 seconds to not break the varnish caching)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve details about a particular event:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  is Event ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    """
    keep_browser_open = True

    def test_001_verify_events_within_page_when_upcomingswitcher_is_selected(self):
        """
        DESCRIPTION: Verify events within page, when 'Upcoming' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: *   Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Event is NOT started
        EXPECTED: *   Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: *   Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: *   Attribute 'isNext24HourEvent="true"' is present
        EXPECTED: *   At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: *   At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: *   At least one market is displayed (available in the response)
        EXPECTED: are shown, when 'Upcoming' sorting type is selected
        EXPECTED: Events with 'isStarted="true"' attribute are NOT present within 'Upcoming' section
        """
        pass
