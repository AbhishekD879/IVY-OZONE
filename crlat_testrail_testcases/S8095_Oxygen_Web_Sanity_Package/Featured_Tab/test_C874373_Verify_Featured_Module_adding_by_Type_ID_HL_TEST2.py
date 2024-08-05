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
class Test_C874373_Verify_Featured_Module_adding_by_Type_ID_HL_TEST2(Common):
    """
    TR_ID: C874373
    NAME: Verify Featured Module adding by Type ID [HL/TEST2]
    DESCRIPTION: This test case verifies Modules configuring in CMS where Module consists of events retrieved by 'Type ID'
    DESCRIPTION: AUTOTESTS [C9690236] [C9697823] [C9690242] [C9690238]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: **Configurations**
    PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section by 'Type ID' via CMS use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
    PRECONDITIONS: 2) For reaching the appropriate CMS per env use the following link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "EventsModule" an choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32612728)
    PRECONDITIONS: 2) Be aware that Live events are not displayed in the 'Featured' modules for Desktop
    """
    keep_browser_open = True

    def test_001_verify_created_module_on_featured_tabsection(self):
        """
        DESCRIPTION: Verify created module on 'Featured' tab/section
        EXPECTED: The created module is displayed and contains the following elements:
        EXPECTED: * Featured module header with module name set in CMS
        EXPECTED: * Odds Card Header (e.g. Home/Draw/Away) is displayed for the module
        EXPECTED: * Number of retrieved events corresponds to Max Events to Display value set in CMS
        EXPECTED: * All events within Module are in date/time range set in CMS
        EXPECTED: * Event Start time/'Live'label/'Match Timer'/'Set'
        EXPECTED: * 'Watch Stream' icon if available
        EXPECTED: * 'Favourite' icon **Football Coral only**
        EXPECTED: * '<number of markets> MORE' link
        EXPECTED: * 'Footer' link set in CMS - only short internal URL should be used(e.x. /virtual-sports/virtual-horse-racing)
        """
        pass

    def test_002_verify_events_order_within_the_module(self):
        """
        DESCRIPTION: Verify Events Order within the module
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1) Live events first:
        EXPECTED: * event displayOrder
        EXPECTED: * event start time
        EXPECTED: * alphabetically
        EXPECTED: 2) Not live events:
        EXPECTED: * event displayOrder
        EXPECTED: * event start time
        EXPECTED: * alphabetically
        """
        pass

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: For Pre-Match events:
        EXPECTED: * For events that occur Today format is 24 hours:
        EXPECTED: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: * For events that occur in the future (including tomorrow) date format is 24 hours:
        EXPECTED: HH:MM, DD MMM (e.g. "14:00 or 05:00, 24 Nov or 02 Nov")
        EXPECTED: For Live events:
        EXPECTED: * Start time is substituted by 'LIVE' label/'Match Timer'/'<number> of Set'
        """
        pass
