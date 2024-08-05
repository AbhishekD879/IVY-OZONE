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
class Test_C2989456_Verify_count_and_order_of_Extra_Place_races_on_Home_page(Common):
    """
    TR_ID: C2989456
    NAME: Verify count and order of 'Extra Place' races on Home page
    DESCRIPTION: This test case verifies count and order of 'Extra Place' races on Home page depending on platform
    PRECONDITIONS: 1. 'Next Races' tab should be present on Home page (click [here](https://ladbrokescoral.testrail.com/index.php?/cases/view/29371) to see how to configure it)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing 'Next Races' tab on Home page
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: **To check info regarding event use the following link:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: **To get info about class events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **To get info about Extra place events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_001_verify_number_of_extra_place_racing_events_shown(self):
        """
        DESCRIPTION: Verify number of 'Extra Place' racing events shown
        EXPECTED: Two 'Extra Place' racing events are shown for **Coral** and one for **Ladbrokes**
        """
        pass

    def test_002_verify_order_of_extra_place_racing_events(self):
        """
        DESCRIPTION: Verify order of 'Extra Place' racing events
        EXPECTED: 'Extra Place' racing events are ordered by 'startTime' attribute from SS response in ascending
        """
        pass
