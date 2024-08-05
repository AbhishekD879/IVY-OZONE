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
class Test_C29382_Verify_events_that_passed_Suspension_Time(Common):
    """
    TR_ID: C29382
    NAME: Verify events that passed "Suspension Time"
    DESCRIPTION: This test case verifies events removing from the 'Featured' tab (mobile/tablet)/ Featured section (desktop) if they passed "Suspension Time"
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-6527 As a TA I want to improve the caching efficiency of Football SiteServer data retrieval
    DESCRIPTION: *   BMA-7859
    DESCRIPTION: *   BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) There are more than one event/selection in the module section
    PRECONDITIONS: 2) CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 3) To retrieve all events for verified Type
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Check "suspendAtTime="YYYY-MM-DDThh:mm:ssZ"" attribute to see the time, when the event should be removed from 'Featured' tab
    PRECONDITIONS: Check **event.suspendAtTime** simple filter in **Networks **
    PRECONDITIONS: The **event.suspendAtTime** simple filter should simply be "2016-01-26T08:26:00.000Z" or "2016-01-26T08:26:30.000Z"
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:18.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:00.000
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:48.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:30.000
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_open_edp_for_event_with_setted_suspended_timecheckeventsuspendattimesimple_filter_innetworksin_console(self):
        """
        DESCRIPTION: Open EDP for event with setted suspended time.
        DESCRIPTION: Check **event.suspendAtTime** simple filter in **Networks **(in Console)
        EXPECTED: The suspendAtTime simple filter should  show the time when event should be removed
        EXPECTED: For example:
        EXPECTED: "2016-01-26T08:26:00.000Z"
        """
        pass

    def test_004_wait_until_time_ofsuspendattimepassed___refresh_page(self):
        """
        DESCRIPTION: Wait until time of **"suspendAtTime" **passed -> Refresh page
        EXPECTED: Verified event is no more shown within module of 'Featured' tab
        """
        pass

    def test_005_repeat_steps_2_3_for_module_created_by_race_typeid_on_the_featured_tab_mobiletablet_featured_section_desktop(self):
        """
        DESCRIPTION: Repeat steps №2-3 for Module created by <Race> typeID on the 'Featured' tab (mobile/tablet)/ Featured section (desktop)
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_3_for_boosted_selection_on_the_featured_tab_mobiletablet_featured_section_desktop(self):
        """
        DESCRIPTION: Repeat steps №2-3 for Boosted Selection on the 'Featured' tab (mobile/tablet)/ Featured section (desktop)
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_3_for_enhanced_multiples_on_the_featured_tab_mobiletablet_featured_section_desktop(self):
        """
        DESCRIPTION: Repeat steps №2-3 for Enhanced Multiples on the 'Featured' tab (mobile/tablet)/ Featured section (desktop)
        EXPECTED: 
        """
        pass
