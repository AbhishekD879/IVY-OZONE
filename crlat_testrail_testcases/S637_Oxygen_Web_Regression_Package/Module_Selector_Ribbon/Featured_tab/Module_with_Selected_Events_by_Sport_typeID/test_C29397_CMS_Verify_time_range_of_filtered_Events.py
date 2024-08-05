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
class Test_C29397_CMS_Verify_time_range_of_filtered_Events(Common):
    """
    TR_ID: C29397
    NAME: CMS: Verify time range of filtered Events
    DESCRIPTION: This test case verifies filtering events to be displayed within Module by time range via CMS
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Category ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving all events for verified type use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&existsFilter=event:simpleFilter:market.isActive&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *   XXX -  is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   YYYY1-MM1-DD1 - is start date
    PRECONDITIONS: *   YYYY2-MM2-DD2 - is end date
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___home_modules(self):
        """
        DESCRIPTION: Go to CMS -> Home Modules
        EXPECTED: 
        """
        pass

    def test_002_tap_create_home_module_button(self):
        """
        DESCRIPTION: Tap 'Create Home Module' button
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_go_to_select_eventsby_field___set_valid_typeid_for_typeenhanced_multiples(self):
        """
        DESCRIPTION: Go to 'Select Events by' field -> set valid 'typeId' for Type/Enhanced Multiples
        EXPECTED: Entered 'typeId' value is shown
        """
        pass

    def test_005_go_to_events_from_and_events_to_fields___click_today_buttons_below_each(self):
        """
        DESCRIPTION: Go to 'Events from' and 'Events to' fields -> Click 'Today' buttons below each
        EXPECTED: Today's date is set correctly in corresponding edit boxes
        """
        pass

    def test_006_click_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Click 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_007_load_invictus_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify events within created Module
        EXPECTED: All events within Module are for the current day
        """
        pass

    def test_008_go_to_cms_home_module_open_created_module_on_the_previous_steps(self):
        """
        DESCRIPTION: Go to CMS->Home Module->open created module on the previous steps
        EXPECTED: 
        """
        pass

    def test_009_go_to_events_from_and_events_to_fields___click_tomorrow_buttons_below_each(self):
        """
        DESCRIPTION: Go to 'Events from' and 'Events to' fields -> Click 'Tomorrow' buttons below each
        EXPECTED: Tomorrow's date is set correctly in corresponding edit boxes
        """
        pass

    def test_010_click_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Click 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_011_load_invictus_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify events within created Module
        EXPECTED: All events within Module are for the next day
        """
        pass

    def test_012_go_to_cms_home_module_open_created_module_on_the_previous_steps(self):
        """
        DESCRIPTION: Go to CMS->Home Module->open created module on the previous steps
        EXPECTED: 
        """
        pass

    def test_013_go_to_events_from_and_events_to_fields___manually_set_date_and_time_range_of_events_that_are_needed_to_be_shown(self):
        """
        DESCRIPTION: Go to 'Events from' and 'Events to' fields -> Manually set date and time range of events that are needed to be shown
        EXPECTED: Corresponding date and time are set in each of edit boxes
        """
        pass

    def test_014_click_load_selection_confirm_selection_save_module_button(self):
        """
        DESCRIPTION: Click 'Load Selection'->'Confirm Selection'->'Save Module' button
        EXPECTED: 
        """
        pass

    def test_015_load_invictus_application_and_verify_events_within_created_module(self):
        """
        DESCRIPTION: Load Invictus application and verify events within created Module
        EXPECTED: All events within Module are in date/time range set in CMS
        """
        pass
