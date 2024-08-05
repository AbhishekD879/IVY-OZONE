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
class Test_C2592701_Verify_displaying_of_ITV_Extra_Place_Races_carousels(Common):
    """
    TR_ID: C2592701
    NAME: Verify displaying of ITV/Extra Place Races carousels
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C11547285](https://ladbrokescoral.testrail.com/index.php?/cases/view/11547285)
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON" (CMS->System configuration->Structure->featuredRaces)
    PRECONDITIONS: 2. There should be NO Horse Racing events with 'Featured Racing Types'(ITV races) or 'Extra Place Race' flags checked in TI
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

    def test_001_verify_module_name_module_displaying(self):
        """
        DESCRIPTION: Verify <Module name> module displaying
        EXPECTED: * <Module name> Module  is not displayed on Featured tab
        """
        pass

    def test_002_go_to_ti_and_check_featured_racing_types_flag_on_any_horse_racing_event(self):
        """
        DESCRIPTION: Go to TI and check 'Featured Racing Types' flag on any Horse Racing event
        EXPECTED: 
        """
        pass

    def test_003_go_back_to_oxygen_application_and_refresh_the_pageverify_module_name_module_displaying(self):
        """
        DESCRIPTION: Go back to oxygen application and refresh the page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * Module can be expanded/collapsed
        EXPECTED: * ITV carousel is displayed
        EXPECTED: * Extra Place Races carousel is not displayed
        """
        pass

    def test_004_verify_displaying_of_events_in_itv_carousel(self):
        """
        DESCRIPTION: Verify displaying of events in ITV carousel
        EXPECTED: **CORAL:**
        EXPECTED: * Event with 'Featured Racing Types' flag is present in ITV carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * Carousel header is displayed
        EXPECTED: * Event race time and meeting name are displayed
        EXPECTED: **LADBROKES:**
        EXPECTED: * Event with 'Featured Racing Types' flag is present in ITV carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * Carousel header and ITV/Extra Place icons are displayed
        EXPECTED: * Event race time and first 4 letters of meeting name are displayed
        """
        pass

    def test_005_go_to_ti_select_any_event_from_step_2_and_check_extra_place_race_flag_on_the_market_level_of_the_selected_event(self):
        """
        DESCRIPTION: Go to TI, select any event from step 2 and check 'Extra Place Race' flag on the market level of the selected event.
        EXPECTED: 
        """
        pass

    def test_006_go_back_to_oxygen_application_and_refresh_the_pageverify_module_name_module_displaying_please_note_that_for_wrappers_changes_will_be_applied_after_5_minutes_change_tab_and_go_back___changes_should_be_applied(self):
        """
        DESCRIPTION: Go back to oxygen application and refresh the page.
        DESCRIPTION: Verify <Module name> module displaying. Please note that for wrappers changes will be applied after 5 minutes (change tab and go back - changes should be applied)
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * ITV carousel is displayed
        EXPECTED: * Extra Place Races carousel is displayed
        """
        pass

    def test_007_verify_displaying_of_events_in_itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of events in ITV and Extra Place Races carousels
        EXPECTED: **CORAL:**
        EXPECTED: * Event is present in Extra Place Races carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * Carousel header is displayed
        EXPECTED: * Event race time and meeting name are displayed
        EXPECTED: **LADBROKES:**
        EXPECTED: * Event with 'Featured Racing Types' flag is present in ITV carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * Carousel header and ITV/Extra Place icons are displayed
        EXPECTED: * Event race time and first 4 letters of meeting name are displayed
        """
        pass

    def test_008_go_to_ti_and_uncheck_featured_racing_types_flag_for_event_from_step_2_that_had_this_flag_checked(self):
        """
        DESCRIPTION: Go to TI and uncheck 'Featured Racing Types' flag for event from Step 2 that had this flag checked
        EXPECTED: 
        """
        pass

    def test_009_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_pageverify_module_name_module_displaying(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * ITV carousel is NOT displayed
        EXPECTED: * Extra Place Races carousel is displayed
        """
        pass

    def test_010_verify_displaying_of_events_in_itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of events in ITV and Extra Place Races carousels
        EXPECTED: **CORAL:**
        EXPECTED: * Event with 'Extra Place Race' flag is present in Extra Place Race carousel
        EXPECTED: * Carousel header is displayed
        EXPECTED: * Event race time and meeting name are displayed
        EXPECTED: **LADBROKES:**
        EXPECTED: * Event with 'Extra Place Race' flag is present in Extra Place Race carousel
        EXPECTED: * Carousel header and ITV/Extra Place icons are displayed
        EXPECTED: * Event race time and first 4 letters of meeting name are displayed
        """
        pass

    def test_011_go_to_ti_and_uncheck_extra_place_race_flag_for_event_from_step_5_that_had_this_flag_checked(self):
        """
        DESCRIPTION: Go to TI and uncheck 'Extra Place Race' flag for event from Step 5 that had this flag checked
        EXPECTED: 
        """
        pass

    def test_012_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_pageverify_module_name_module_displaying(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> module is NOT displayed
        EXPECTED: * ITV and Extra Place Races carousels are NOT displayed
        """
        pass
