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
class Test_C9618071_Races_displaying_races_in_Offers_Featured_Races_section(Common):
    """
    TR_ID: C9618071
    NAME: <Races>: displaying races in 'Offers & Featured Races' section
    DESCRIPTION: This test case verifies displaying of <Races> in 'Offers & Featured Races' section
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have next Horse Race events:
    PRECONDITIONS: 1) With enabled 'Featured Racing Types' check box on event level (drilldownTagNames="EVFLAG_FRT") and races should be from different types
    PRECONDITIONS: 2) With enabled 'Extra Place Race' check box on market level (drilldownTagNames="MKTFLAG_EPR") and races should be from different types
    PRECONDITIONS: - You should be on Horse Racing landing page
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

    def test_001_verify_displaying_of_offers__featured_races_section(self):
        """
        DESCRIPTION: Verify displaying of 'Offers & Featured Races' section
        EXPECTED: 'Offers & Featured Races' section is shown
        """
        pass

    def test_002_verify_displaying_of_the_events_with_enabled_featured_racing_types_check_box(self):
        """
        DESCRIPTION: Verify displaying of the events with enabled 'Featured Racing Types' check box
        EXPECTED: - Events are displayed in "ITV Races" sub category within 'Offers & Featured Races' section
        EXPECTED: - 'ITV' icon is shown at the top right corner of the sub category
        EXPECTED: - First 4-5 letters of race type are displayed under race time
        """
        pass

    def test_003_verify_displaying_of_the_events_with_enabled_extra_place_race_check_box(self):
        """
        DESCRIPTION: Verify displaying of the events with enabled 'Extra Place Race' check box
        EXPECTED: - The event is displayed in "Extra Place Offer" sub category within 'Offers & Featured Races' section
        EXPECTED: - 'Extra Place' icon is shown at the top right corner of the sub category
        EXPECTED: - First 4-5 letters of race type are displayed under race time
        """
        pass
