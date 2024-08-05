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
class Test_C2807727_Delayed_Races_are_removed_when_flag_is_off_Y_is_received(Common):
    """
    TR_ID: C2807727
    NAME: Delayed Races are removed when flag "is_off = Y" is received
    DESCRIPTION: Test case verifies that delayed races disappear from Next Races carousel when flag "is_off = Y" is received
    DESCRIPTION: AUTOTEST [C2911646]
    DESCRIPTION: AUTOTEST [C2911648]
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
    PRECONDITIONS: **User is on Horse Racing landing page. Delayed event is available on Next Races carousel**
    """
    keep_browser_open = True

    def test_001_in_ti_on_the_event_level_set_isoff__yes_for_the_delayed_event(self):
        """
        DESCRIPTION: In TI on the event level set IsOff = Yes for the delayed event
        EXPECTED: Event disappears from Next Races carousel in real time
        """
        pass
