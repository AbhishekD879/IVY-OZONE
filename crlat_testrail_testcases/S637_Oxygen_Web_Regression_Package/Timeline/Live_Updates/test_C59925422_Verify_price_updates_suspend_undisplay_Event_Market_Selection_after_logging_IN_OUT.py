import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C59925422_Verify_price_updates_suspend_undisplay_Event_Market_Selection_after_logging_IN_OUT(Common):
    """
    TR_ID: C59925422
    NAME: Verify price updates, suspend/undisplay Event/Market/Selection after logging IN/OUT
    DESCRIPTION: This test case verifies price updates, suspend/undisplay Event/Market/Selection after logging IN/OUT
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Timeline should be enabled in CMS
    PRECONDITIONS: 2.Live Campaign is created
    PRECONDITIONS: 3.Timeline posts with prices are created and published
    PRECONDITIONS: 4.Load the app
    PRECONDITIONS: 5.User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: 6.Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline should be opened and displayed in the expanded state
        EXPECTED: ->Configured Post with a Price/Odds button is displayed
        EXPECTED: ->'POST' response should be present with all fields form CMS in WS.
        """
        pass

    def test_002_log_out_from_the_app(self):
        """
        DESCRIPTION: Log Out from the app
        EXPECTED: - User is logged out
        EXPECTED: - Timeline is **NOT** displayed in the app
        """
        pass

    def test_003_price_changenavigate_to_the_ti_backoffice_and_change_price_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: **Price Change**
        DESCRIPTION: Navigate to the TI (backoffice) and change price for the selection for the Timeline Post
        EXPECTED: - Price is changed and saved for the selection in the TI (backoffice)
        """
        pass

    def test_004_log_in_to_the_app_and_open_timeline(self):
        """
        DESCRIPTION: Log in to the app and open Timeline
        EXPECTED: - Timeline WS is opened
        EXPECTED: - Price is changed for Post in the Timeline
        """
        pass

    def test_005_log_out_from_the_app(self):
        """
        DESCRIPTION: Log Out from the app
        EXPECTED: - User is logged out
        EXPECTED: - Timeline is **NOT** displayed in the app
        """
        pass

    def test_006_suspensionnavigate_to_the_ti_backoffice_and_suspend_eventmarketselection_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: **Suspension**
        DESCRIPTION: Navigate to the TI (backoffice) and suspend Event/Market/Selection for the selection for the Timeline Post
        EXPECTED: - Changes are saved successfully in the TI (backoffice)
        EXPECTED: - Event/Market/Selection is suspended
        """
        pass

    def test_007_log_in_to_the_app_and_open_timeline(self):
        """
        DESCRIPTION: Log in to the app and open Timeline
        EXPECTED: - Timeline WS is opened
        EXPECTED: - Price/Odds button  is displayed as greyed out and becomes disabled
        """
        pass

    def test_008_log_out_from_the_app(self):
        """
        DESCRIPTION: Log Out from the app
        EXPECTED: - User is logged out
        EXPECTED: - Timeline is **NOT** displayed in the app
        """
        pass

    def test_009_navigate_to_the_ti_backoffice_and_do_active_eventmarketselection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and do ACTIVE Event/Market/Selection for the Timeline Post
        EXPECTED: - Changes are saved successfully in the TI (backoffice)
        EXPECTED: - Event/Market/Selection is Active
        """
        pass

    def test_010_log_in_to_the_app_and_open_timeline(self):
        """
        DESCRIPTION: Log in to the app and open Timeline
        EXPECTED: - Timeline WS is opened
        EXPECTED: - Price/Odds button is displayed as active and enabled (clickable) with prices
        """
        pass

    def test_011_undisplayingrepeat_steps_5_10_for_undisplayingdisplaying_eventmarketselection_in_the_ti_backoffice_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: **Undisplaying**
        DESCRIPTION: Repeat steps 5-10 for Undisplaying/Displaying Event/Market/Selection in the TI (backoffice) for the selection for the Timeline Post
        EXPECTED: **Undisplaying**
        EXPECTED: - **'N/A'** is displayed as greyed out and disabled for the selection for the Post instead of the Price/Odds
        EXPECTED: ![](index.php?/attachments/get/119657446)
        """
        pass
