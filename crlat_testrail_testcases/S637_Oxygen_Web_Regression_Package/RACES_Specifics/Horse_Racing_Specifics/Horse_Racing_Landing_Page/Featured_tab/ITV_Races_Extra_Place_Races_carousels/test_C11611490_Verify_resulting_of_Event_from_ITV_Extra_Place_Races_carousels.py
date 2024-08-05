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
class Test_C11611490_Verify_resulting_of_Event_from_ITV_Extra_Place_Races_carousels(Common):
    """
    TR_ID: C11611490
    NAME: Verify resulting of Event from ITV/Extra Place Races carousels
    DESCRIPTION: This test case verifies resulting of Event from ITV/Extra Place Races carousels
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [С11809206](https://ladbrokescoral.testrail.com/index.php?/cases/view/11809206)
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON" (CMS->System configuration->Structure->featuredRaces)
    PRECONDITIONS: 2. There should be few Horse Racing events configured with 'Featured Racing Types'(ITV races), 'Extra Place Race'  and with both flags checked in TI.
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page.
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level
    PRECONDITIONS: 'Extra Place Race' flag - is checked on market level
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

    def test_001_verify_displaying_of__itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of  ITV and Extra Place Races carousels
        EXPECTED: * ITV and Extra Place Races carousels are displayed on Horse Racing Featured tab
        EXPECTED: * Events from preconditions are displayed in the related carousels.
        """
        pass

    def test_002_in_ti_select_three_events_from_preconditions1_with_featured_racing_types_flag_1_with_extra_place_race_flag_and_1_with_both_flags_checked_and_set_results_for_themevents_are_considered_as_resulted(self):
        """
        DESCRIPTION: In TI select three events from preconditions(1 with 'Featured Racing Types' flag, 1 with 'Extra Place Race' flag and 1 with both flags checked) and set results for them(events are considered as resulted)
        EXPECTED: 
        """
        pass

    def test_003_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_pageverify_that_resulted_events_are_removed_from_module_automatically(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify that resulted events are removed from module automatically
        EXPECTED: * Resulted event with 'Featured Racing Types' flag is removed from ITV carousel by live update
        EXPECTED: * Resulted event with 'Extra Place Race' flag is removed from Extra Place Races carousel by live update
        EXPECTED: * Resulted event with both 'Featured Racing Types' and ''Extra Place Race' flags is removed from both carousels by live update.
        EXPECTED: * Not resulted events are still displayed in ITV and Extra place
        """
        pass
