import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C29429_Event_Section_Content(Common):
    """
    TR_ID: C29429
    NAME: Event Section Content
    DESCRIPTION: This test case verifies event section content of module created by 'Race Grid' option within 'Featured' tab
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8776 Decouple HR Grid and make it available for Featured Tab
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **'Name' **attribute to see an event local time
    PRECONDITIONS: 'T**ypeName'** attribute to see 'Race Meetings' name.
    PRECONDITIONS: 4) HR Grid module is added in CMS on Featured tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Feature' tab is selected by default
        """
        pass

    def test_002_go_to_module_selector_ribbon___featured_tab___module_created_by_race_grid_option(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon -> Featured tab -> Module created by 'Race Grid' option
        EXPECTED: Module created by 'Race Grid' option is shown
        """
        pass

    def test_003_verify_list_of_race_meetings(self):
        """
        DESCRIPTION: Verify list of race meetings
        EXPECTED: Each race meeting name corresponds to the '**typeName'** attribute from the Site Server response
        """
        pass

    def test_004_verify_events_displaying(self):
        """
        DESCRIPTION: Verify events displaying
        EXPECTED: *   Events off times are displayed horizontally across the page
        EXPECTED: *   Each event off time is located in a separate section
        EXPECTED: *   Events off times with LP prices are displayed in bold if **'priceTypeCodes="LP,"'** attribute is available for **'Win or Each way'** market only
        """
        pass

    def test_005_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times
        EXPECTED: Ability to scroll left and right is available
        """
        pass

    def test_006_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times
        EXPECTED: *   Event off times corresponds to the race local time from the '**name'** attribute from the Site Server
        EXPECTED: *   Only events on current date are present on Race grid
        """
        pass

    def test_007_click__tap_on_event_off_time(self):
        """
        DESCRIPTION: Click / tap on event off time
        EXPECTED: Event Details page is opened
        """
        pass
