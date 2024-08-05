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
class Test_C29414_Verify_Race_events_carousel_Data(Common):
    """
    TR_ID: C29414
    NAME: Verify <Race> events carousel Data
    DESCRIPTION: This test case is for checking a data which is displayed in <Race> events carousel of module created by <Race> type ID within Featured tab
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    DESCRIPTION: AUTOTEST [C13135243]
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event name and local time
    PRECONDITIONS: - **'typeFlagCodes' **to check event group
    PRECONDITIONS: - **'eventStatusCode'** to check whether event is active or suspended
    PRECONDITIONS: - **'marketStatusCode' **to see market status
    PRECONDITIONS: - **'outcomeStatusCode'** to see outcome status
    PRECONDITIONS: 4) Invictus application is loaded
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
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

    def test_003_check_race_events_carousel_within_verified_module(self):
        """
        DESCRIPTION: Check <Race> events carousel within verified module
        EXPECTED: <Race> events carousel is displayed below the module header
        """
        pass

    def test_004_verify_data_in_race_events_carousel(self):
        """
        DESCRIPTION: Verify data in <Race> events carousel
        EXPECTED: - Races retrieved by typeID in CMS are shown
        EXPECTED: - Data corresponds to the Site Server response.
        EXPECTED: See attribute **'name'**.
        EXPECTED: - Events are sorted by **'start time'**: the first event to start is shown first.
        """
        pass

    def test_005_verify_events_which_are_displayed_in_the_race_events_carousel(self):
        """
        DESCRIPTION: Verify events which are displayed in the <Race> events carousel
        EXPECTED: *   Only active events are displayed in the <Race> events carousel (for those events attribute **'eventStatusCode'**='A' in the Site Server response)
        EXPECTED: *   Only events with active markets are shown in the <Race> events carousel (**'marketStatusCode'**='A')
        """
        pass

    def test_006_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: *   3 selection in the event are shown
        EXPECTED: *   Only active selections are shown (**'outcomeStatusCode'**='A')
        """
        pass
