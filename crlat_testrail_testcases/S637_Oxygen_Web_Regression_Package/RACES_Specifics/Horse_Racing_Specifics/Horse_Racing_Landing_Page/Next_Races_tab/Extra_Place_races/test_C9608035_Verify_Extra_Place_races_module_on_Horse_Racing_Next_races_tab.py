import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C9608035_Verify_Extra_Place_races_module_on_Horse_Racing_Next_races_tab(Common):
    """
    TR_ID: C9608035
    NAME: Verify 'Extra Place' races module on Horse Racing > 'Next races' tab
    DESCRIPTION: This test case verifies how 'Extra Place' races module look like on Horse Racing > 'Next Races' tab
    DESCRIPTION: AUTOTEST : C17505270
    PRECONDITIONS: 1. "Next Races" tab for Horse Racing EDP should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing Horse Racing EDP
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: **To check info regarding event use the following link:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: **To configure 'Extra Place' signposting icon:**
    PRECONDITIONS: 1) Open CMS -> Promotions ->  EXTRA PLACE RACE (if promotion is configured in another case use the instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Promotions+CMS+configuration).
    PRECONDITIONS: 2) Required fields for CMS configuration of created EXTRA PLACE RACE promotion:
    PRECONDITIONS: * 'Is Signposting Promotion' checkbox (should be checked for activation Promo SIgnposting for different promotions)
    PRECONDITIONS: * 'Event-level flag' field
    PRECONDITIONS: * 'Market-level flag' field
    PRECONDITIONS: * 'Overlay BET NOW button url' field (not required but without current URL 'BET NOW' button will be unclickable)
    PRECONDITIONS: * 'Promotion Text' field (for editing promo footer text / not required)
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

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: 'Next Races' tab contains:
        EXPECTED: - 'Extra Place' races module
        EXPECTED: - 'Next Races' module (if configured)
        """
        pass

    def test_002_verify_extra_place_content_area(self):
        """
        DESCRIPTION: Verify 'Extra Place' content area
        EXPECTED: Contains:
        EXPECTED: - 'Extra place' signposting icon (if configured)
        EXPECTED: - Event time (corresponds to **'startTime'** in SS response)
        EXPECTED: - Event name (taken from event **'name'** from SS response)
        EXPECTED: - Going (corresponds to **'going'** within **'racingFormEvent'** section from SS response)
        EXPECTED: - Distance (corresponds to **'distance'** within 'racingFormEvent' section from SS response)
        EXPECTED: - 'Each Way' terms (correspond to **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes in SS response)
        EXPECTED: - '>' icon
        """
        pass

    def test_003_verify_each_way_terms_displaying(self):
        """
        DESCRIPTION: Verify 'Each Way' terms displaying
        EXPECTED: 'Each Way' terms are displayed if **isEachWayAvailable = true** attribute is present in SS response
        """
        pass
