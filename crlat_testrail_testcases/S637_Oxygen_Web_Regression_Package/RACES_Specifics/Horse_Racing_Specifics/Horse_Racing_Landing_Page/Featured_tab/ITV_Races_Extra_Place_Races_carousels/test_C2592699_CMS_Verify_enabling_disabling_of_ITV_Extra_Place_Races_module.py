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
class Test_C2592699_CMS_Verify_enabling_disabling_of_ITV_Extra_Place_Races_module(Common):
    """
    TR_ID: C2592699
    NAME: [CMS] Verify enabling/disabling of ITV/Extra Place Races module
    DESCRIPTION: This test case verifies enabling/disabling of ITV/Extra Place Races carousels.
    PRECONDITIONS: 1. Make sure there are Horse Racing events with 'Featured race'(ITV races) or 'Extra place' flags checked in TI.
    PRECONDITIONS: 2. Feature toggle in CMS is disabled
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level'Extra place' flag - is checked on market level
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

    def test_001_verify_that_module_name_module_is_not_displayed(self):
        """
        DESCRIPTION: Verify that <Module name> Module is not displayed
        EXPECTED: * <Module name> Module is not displayed on Featured tab
        EXPECTED: * ITV and Extra Place Races carousels are not displayed
        """
        pass

    def test_002_go_to_cms_set_module_name_module_toggle_to_on_and_save_changesrefresh_the_horse_racing_landing_page_in_application_and_verify_module_displaying(self):
        """
        DESCRIPTION: Go to CMS, set <Module name> Module toggle to "ON" and save changes.
        DESCRIPTION: Refresh the Horse Racing landing page in application and verify Module displaying.
        EXPECTED: * <Module name> Module is displayed on Featured tab
        EXPECTED: * ITV and Extra Place Races carousels are displayed with related events inside
        EXPECTED: * Signposting icons are displayed
        """
        pass

    def test_003_navigate_to_other_tabs_present_on_horse_racing_pageeg_antepost_specials_yourcall_results_and_verify_module_name_module_displaying(self):
        """
        DESCRIPTION: Navigate to other tabs present on Horse Racing page(e.g. Antepost, Specials, Yourcall, Results) and Verify <Module name> Module displaying.
        EXPECTED: * <Module name> Module is not displayed on other tabs present on Horse Racing page.
        EXPECTED: * ITV and Extra Place Races carousels are not displayed
        """
        pass

    def test_004_go_to_cms_set_module_name_module_toggle_to_off_and_save_changesrefresh_the_horse_racing_landing_page_in_application_and_verify_module_displaying(self):
        """
        DESCRIPTION: Go to CMS, set <Module name> Module toggle to "OFF" and save changes.
        DESCRIPTION: Refresh the Horse Racing landing page in application and verify Module displaying.
        EXPECTED: * <Module name> Module is not displayed on Featured tab
        EXPECTED: * ITV and Extra Place Races carousels are not displayed
        """
        pass
