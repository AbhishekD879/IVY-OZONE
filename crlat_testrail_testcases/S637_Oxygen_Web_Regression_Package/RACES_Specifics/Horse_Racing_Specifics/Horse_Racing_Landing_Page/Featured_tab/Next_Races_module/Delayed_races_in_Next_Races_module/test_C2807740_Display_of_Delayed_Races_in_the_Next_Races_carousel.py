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
class Test_C2807740_Display_of_Delayed_Races_in_the_Next_Races_carousel(Common):
    """
    TR_ID: C2807740
    NAME: Display of Delayed Races in the Next Races carousel
    DESCRIPTION: Test case verifies that delayed races are displayed in the Next Races carousel
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure > Next Races
    PRECONDITIONS: **Events are derived from the following request:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: Delayed event has start time of 1 hr (or less) ago and flags "is_off = N"
    PRECONDITIONS: **User is on Horse Racing landing page**
    """
    keep_browser_open = True

    def test_001_create_edit_event_with_start_time_in_the_range_from_current_time___1hr__to_current_time_and_flag_is_off__no(self):
        """
        DESCRIPTION: Create (edit) event with start time in the range from [current time - 1hr]  to [current time] and flag "is_off = No"
        EXPECTED: Delayed event in the time range from [current time - 1hr] to [current time] and flag "is_off = No" is displayed in the Next races carousel
        """
        pass

    def test_002_create_edit_event_with_start_time_of_current_time___1hr_and_flag_is_off__no(self):
        """
        DESCRIPTION: Create (edit) event with start time of [current time - 1hr] and flag "is_off = No"
        EXPECTED: Delayed event with start time of [current time - 1hr] and flag "is_off = No" is displayed in the Next races carousel
        """
        pass
