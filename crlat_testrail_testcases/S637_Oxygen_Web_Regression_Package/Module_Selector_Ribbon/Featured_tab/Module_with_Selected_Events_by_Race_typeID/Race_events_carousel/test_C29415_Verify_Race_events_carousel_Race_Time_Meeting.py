import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29415_Verify_Race_events_carousel_Race_Time_Meeting(Common):
    """
    TR_ID: C29415
    NAME: Verify <Race> events carousel Race Time & Meeting
    DESCRIPTION: This test case if for checking correctness of <Race> events carousel race time and meeting
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    DESCRIPTION: AUTOTEST Mobile: [C2593111]
    DESCRIPTION: AUTOTEST Desktop: [C2746077]
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event name and local time
    PRECONDITIONS: - **'typeName'** to check a race meeting name
    PRECONDITIONS: - **isEachWayAvailable, eachWayFactorDen, ​eachWayPlaces, ​eachWayFactorNum **to check if there are each way terms
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 4) Invictus application is loaded
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
        """
        pass

    def test_002_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_003_verify_event_section_header_of_race_events_carousel(self):
        """
        DESCRIPTION: Verify event section header of <Race> events carousel
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: Race event section header is shown in the following format:
        EXPECTED: * 'HH:MM EventName'
        EXPECTED: * E/W x/y odds - places z-j-k
        EXPECTED: Example: "3:25 York E/W 1/4 odds - places 1-2"
        EXPECTED: Text IS NOT clickable
        EXPECTED: **For Desktop:**
        EXPECTED: Race event section header is shown in the following format: 'HH:MM EventName'
        """
        pass

    def test_004_for_mobiletabletverify_each_way_terms_in_event_section_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Verify each way terms in event section header
        EXPECTED: Each way terms are shown if **isEachWayAvailable='true'**
        EXPECTED: EachWay terms are formed from the following attributes:
        EXPECTED: ***" E/W x/y odds - places z-j-k"***
        EXPECTED: where:
        EXPECTED: x = eachWayFactorNum
        EXPECTED: y= eachWayFactorDen
        EXPECTED: z-j-k = eachWayPlaces
        """
        pass

    def test_005_verify_race_meeting_correctness(self):
        """
        DESCRIPTION: Verify race meeting correctness
        EXPECTED: Race Meeting name corresponds to the SiteServer response.
        EXPECTED: From the list of events look at the attribute **'typeName'** near the selected event
        EXPECTED: Event time corresponds to the race local time ( see** 'name' **attribute from the Site Server response)
        """
        pass
