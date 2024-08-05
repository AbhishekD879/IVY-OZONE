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
class Test_C9608037_Verify_count_and_order_of_Extra_Place_races_on_Horse_Racing_Next_races_tab(Common):
    """
    TR_ID: C9608037
    NAME: Verify count and order of 'Extra Place' races on Horse Racing > 'Next races' tab
    DESCRIPTION: This test case verifies count and order of 'Extra Place' races on Home page depending on platform
    PRECONDITIONS: 1. "Next Races" tab for Horse Racing EDP should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing 'Next Races' tab on Horse Racing landing page
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: **NOTE:** Two or more events should be configured and displayed on the HR landing page in the "Extra Place Offer" section.
    PRECONDITIONS: **To check info regarding event use the following link:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: **The requests to check 'Offers' data (Extra Place, ITV) on Homepage/'Next Races' tab (Coral and Ladbrokes) and HR Landing page/'Next Races' tab (Ladbrokes only):**
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToMarketForClass/35073,16323,16322,16334,390,35103,228,227,226,225,224,223,321?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&translationLang=en&responseFormat=json
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToMarketForClass/16323,16322,390,228,227,226,225,224,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&translationLang=en&responseFormat=json
    PRECONDITIONS: **The requests to check 'Offers' data (Extra Place, ITV) on HR Landing page/'Featured' tab ('Meetings' tab on Ladbrokes brand):**
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/35073,16323,16322,16334,390,35103,228,227,226,225,224,223,321?simpleFilter=event.categoryId:intersects:21&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR&simpleFilter=event.startTime:greaterThanOrEqual:2020-07-09T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-07-15T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-07-09T08:57:30.000Z&simpleFilter=event.classId:notIntersects:227&existsFilter=event:simpleFilter:market.drilldownTagNames:notIntersects:MKTFLAG_SP&simpleFilter=event.drilldownTagNames:notContains:EVFLAG_AP&externalKeys=event&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/16323,16322,390,228,227,226,225,224,223?simpleFilter=event.categoryId:intersects:21&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR&simpleFilter=event.startTime:greaterThanOrEqual:2020-07-09T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-07-15T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-07-09T09:02:00.000Z&simpleFilter=event.classId:notIntersects:227&existsFilter=event:simpleFilter:market.drilldownTagNames:notIntersects:MKTFLAG_SP&simpleFilter=event.drilldownTagNames:notContains:EVFLAG_AP&externalKeys=event&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_go_to_the_hr__next_races_tab(self):
        """
        DESCRIPTION: Go to the HR > "Next races" tab
        EXPECTED: The tab is opened. "Extra Place" module is displayed.
        """
        pass

    def test_002_verify_the_number_of_extra_place_racing_events_shown(self):
        """
        DESCRIPTION: Verify the number of 'Extra Place' racing events shown
        EXPECTED: Only one first 'Extra Place' racing event is shown in the "Extra Place" module on the "Next races" tab.
        """
        pass
