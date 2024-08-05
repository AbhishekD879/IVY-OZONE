import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29394_CMS_Verify_Events_Retrieving_by_TypeID(Common):
    """
    TR_ID: C29394
    NAME: CMS: Verify Events Retrieving by TypeID
    DESCRIPTION: This test case verifies Events Retrieving by TypeID
    DESCRIPTION: Note: Test Case should cover all supporting Sports. Sould be verified on mobile, tablet and desktop.
    DESCRIPTION: Jira ticket: BMA-8200 Desktop - Hide in-play Events on Featured Tab
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS -> Featured Tab Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Tap 'Create Featured Tab Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data_make_sure_that_module_will_be_visible_on_mobile_tablet_and_desktop(self):
        """
        DESCRIPTION: Fill in all required fields with valid data (make sure that Module will be visible on Mobile, Tablet, and Desktop)
        EXPECTED: 
        """
        pass

    def test_004_go_to_select_eventsby_field_and_select_type_id(self):
        """
        DESCRIPTION: Go to 'Select Events by' field and select **Type ID**
        EXPECTED: 
        """
        pass

    def test_005_set_valid_type_id_what_includes_in_play_and_pre_match_events(self):
        """
        DESCRIPTION: Set valid Type ID (what includes In-Play and Pre-Match Events)
        EXPECTED: Entered Type ID is shown
        """
        pass

    def test_006_select_appropriate_date_range_events_from_to(self):
        """
        DESCRIPTION: Select appropriate Date range (Events From-to)
        EXPECTED: Date range is selected
        """
        pass

    def test_007_tap_load_selection(self):
        """
        DESCRIPTION: Tap 'Load Selection'
        EXPECTED: * In-Play Events are loaded  (Events with attribute:
        EXPECTED: drilldownTagNames="EVFLAG_BL"
        EXPECTED: isMarketBetInRun = "true"
        EXPECTED: isLiveNowEvent="true")
        EXPECTED: * Pre-Match Events are loaded (Events with attribute:
        EXPECTED: isNext24HourEvent="true")
        EXPECTED: * Finished Events are NOT loaded (Events with attribute:
        EXPECTED: isFinished=true)
        """
        pass

    def test_008_trigger_the_following_situation_for_one_of_in_play_sport_eventisfinishedtrue(self):
        """
        DESCRIPTION: Trigger the following situation for one of In-Play <Sport> event:
        DESCRIPTION: *isFinished=true*
        EXPECTED: 
        """
        pass

    def test_009_tap_load_selection(self):
        """
        DESCRIPTION: Tap 'Load Selection'
        EXPECTED: * Current In-Play Event is NOT loaded
        EXPECTED: * All other In-Play Events are loaded
        EXPECTED: * Pre-Match Events are loaded
        EXPECTED: * Finished Events are NOT loaded
        """
        pass

    def test_010_tap_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Tap 'Confirm Selection'->'Save Module' button
        EXPECTED: Events are correctly displayed with the following order rules:
        EXPECTED: 1. By SiteServer event Display Order
        EXPECTED: if the same display order then
        EXPECTED: 2. By Start time
        EXPECTED: if the same start time then
        EXPECTED: 3. By Name
        """
        pass

    def test_011_load_invictus_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify events within created Module
        EXPECTED: All events have the same TypeId as was set on step №5
        """
        pass

    def test_012_verify_that_in_play_events_are_displayed_in_the_featured_module_on_mobile_and_tablet(self):
        """
        DESCRIPTION: Verify that In-Play events are displayed in the Featured Module on Mobile and Tablet
        EXPECTED: In-Play events (with attributes: *drilldownTagNames="EVFLAG_BL"* , *isMarketBetInRun = "true"* and *isLiveNowEvent="true"*) are displayed on Mobile and Tablet
        """
        pass

    def test_013_verify_that_in_play_events_are_not_displayed_in_the_featured_module_on_desktop(self):
        """
        DESCRIPTION: Verify that In-Play events are NOT displayed in the Featured Module on desktop
        EXPECTED: In-Play events (with attributes: *drilldownTagNames="EVFLAG_BL"* , *isMarketBetInRun = "true"* and *isLiveNowEvent="true"*) are NOT displayed on desktop.
        """
        pass
