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
class Test_C878819_Verify_Featured_Module_adding_by_Selection_ID_Boosted_Selections_HL_TEST2(Common):
    """
    TR_ID: C878819
    NAME: Verify Featured Module adding by Selection ID (Boosted Selections)  [HL/TEST2]
    DESCRIPTION: This test case verifies Modules configured in CMS where Module consists of one selection retrieved by 'Selection ID'
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: **Configurations**
    PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section by 'Selection ID' via CMS use the following instruction:
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
        EXPECTED: * 'Featured' module header with module name set in CMS
        EXPECTED: * 'Specials' or 'Enhanced' label in the header if it set in CMS
        EXPECTED: * Card with 'Selection' name and 'Price/Odds' button
        EXPECTED: * Event Start time
        EXPECTED: * 'Watch Stream' icon if available
        EXPECTED: * 'Favourite' icon **Football Coral only**
        EXPECTED: * 'Footer' link set in CMS
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection' name
        EXPECTED: * 'Selection' name within module corresponds to <name> attribute the response OR to <name> set in CMS if name was overridden
        EXPECTED: * 'Selection' long name is wrapped into a few lines without cutting the text
        """
        pass

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: * 'Event Start Time' corresponds to 'startTime' attribute
        EXPECTED: *  For events that occur Today format is 24 hours:
        EXPECTED: HH:MM, Today (e.g. "14:00 or 05:00 Today").
        EXPECTED: *   For events that occur in the future (including tomorrow) date format is 24 hours:
        EXPECTED: HH:MM DD MMM (e.g. "14:00 or 05:00 24 Nov or 02 Nov")
        EXPECTED: * Start time is not displayed for started events
        """
        pass

    def test_004_verify_live_label_for_mobiletablet_only(self):
        """
        DESCRIPTION: Verify 'Live' label **For Mobile/Tablet only**
        EXPECTED: 'LIVE' label is shown if event is started
        """
        pass

    def test_005_verify_priceodds_button_within_the_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within the created Module
        EXPECTED: 'Price/Odds' button is shown with the correct price of the selection
        """
        pass
