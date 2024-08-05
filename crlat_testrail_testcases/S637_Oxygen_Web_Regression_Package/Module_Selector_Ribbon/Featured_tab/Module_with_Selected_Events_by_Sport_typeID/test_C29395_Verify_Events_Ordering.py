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
class Test_C29395_Verify_Events_Ordering(Common):
    """
    TR_ID: C29395
    NAME: Verify Events Ordering
    DESCRIPTION: This test case verifies Event Filtering and Ordering within module.
    PRECONDITIONS: 1) There are more than two events in the module section
    PRECONDITIONS: 2) CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
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

    def test_003_verify_events_order(self):
        """
        DESCRIPTION: Verify Events Order
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1) Live events first (Mobile only) (rawIsOffCode="Y" OR (isStated="true" AND rawIsOffCode="-")):
        EXPECTED: *   event displayOrder
        EXPECTED: *   event start time
        EXPECTED: *   alphabetically
        EXPECTED: 2) Not live events:
        EXPECTED: *   event displayOrder
        EXPECTED: *   event start time
        EXPECTED: *   alphabetically
        """
        pass

    def test_004_verify_events_filtering(self):
        """
        DESCRIPTION: Verify Events Filtering
        EXPECTED: Events which are configured on CMS are shown
        EXPECTED: Undisplayed events are hidden from the front end
        """
        pass
