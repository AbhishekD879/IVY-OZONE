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
class Test_C2593956_Verify_navigation_through_ITV_Races_Extra_Place_Races_carousels(Common):
    """
    TR_ID: C2593956
    NAME: Verify navigation through ITV Races/Extra Place Races carousels
    DESCRIPTION: This test case verifies navigation through ITV Races/Extra Place Races carousels
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C11508491](https://ladbrokescoral.testrail.com/index.php?/cases/view/11508491)
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON"
    PRECONDITIONS: 2. There should be enough Horse Racing events with 'Featured race'(ITV races) flag and with 'Extra place' flags configured in TI so they can't fit the width of the screen.
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page.
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level
    PRECONDITIONS: 'Extra place' flag - is checked on market level
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

    def test_001_verify_module_name_module__displaying(self):
        """
        DESCRIPTION: Verify <Module name> Module  displaying
        EXPECTED: * <Module name> Module is displayed on Featured tab
        EXPECTED: * ITV and Extra Place Races carousels are displayed with related events inside
        EXPECTED: * ITV and Extra Place Races are displayed as separate carousels
        """
        pass

    def test_002_verify_navigation_through_itv_carousel(self):
        """
        DESCRIPTION: Verify navigation through ITV carousel
        EXPECTED: * User is able to navigate through carousels by swiping through
        EXPECTED: * Extra Place Races carousel remains untouched while navigation through ITV carousel
        """
        pass

    def test_003_verify_navigation_through_extra_place_races_carousel(self):
        """
        DESCRIPTION: Verify navigation through Extra Place Races carousel
        EXPECTED: * User is able to navigate through carousels by swiping through
        EXPECTED: * ITV Races carousel remains untouched while navigation through Extra Place Races carousel
        """
        pass
