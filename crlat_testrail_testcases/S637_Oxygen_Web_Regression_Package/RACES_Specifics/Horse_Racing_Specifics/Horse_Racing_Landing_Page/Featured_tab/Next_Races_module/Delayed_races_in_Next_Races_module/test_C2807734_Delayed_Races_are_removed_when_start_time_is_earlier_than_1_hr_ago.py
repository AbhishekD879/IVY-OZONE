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
class Test_C2807734_Delayed_Races_are_removed_when_start_time_is_earlier_than_1_hr_ago(Common):
    """
    TR_ID: C2807734
    NAME: Delayed Races are removed when start time is earlier than 1 hr ago
    DESCRIPTION: Test case verifies that event with start time earlier than 1 hr ago isn't displayed in the next races carousel
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure > Next Races
    PRECONDITIONS: **Events are derived from the following request:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: Delayed event has start time of 1 hr or less ago and "is_off = N" flag.
    PRECONDITIONS: **User is on Horse Racing landing page. Horse Racing delayed event is available on Next Races carousel**
    """
    keep_browser_open = True

    def test_001_edit_delayed_event_start_time_to_haveevent_with_start_time_current_time___1hr_2_mins_and_flag_isoff__no(self):
        """
        DESCRIPTION: Edit delayed event start time to have:
        DESCRIPTION: event with start time [current time] - 1hr 2 mins and flag IsOff = No
        EXPECTED: Delayed event which has start time earlier than 1 hr ago disappears from Next Races carousel
        """
        pass
