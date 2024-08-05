import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@vtest
class Test_C59925421_Verify_undisplaying_Event_Market_Selection_for_the_Timeline_Post(Common):
    """
    TR_ID: C59925421
    NAME: Verify undisplaying Event/Market/Selection for the Timeline Post
    DESCRIPTION: This test case verifies undisplaying Event/Market/Selection for the Timeline Post
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Timeline should be enabled in CMS
    PRECONDITIONS: 2.Live Campaign is created.
    PRECONDITIONS: 3.Timeline posts with prices are created and published
    PRECONDITIONS: 4.Load the app
    PRECONDITIONS: 5.User is logged in
    PRECONDITIONS: 6.Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: Sport/Races
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Ladbrokes- Ladbrokes Lounge
    PRECONDITIONS: Coral-Coral Pulse
    """
    keep_browser_open = True

    def test_001_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: Timeline should be opened and displayed in the expanded state
        EXPECTED: Configured Post with a Price/Odds button is displayed
        """
        pass

    def test_002_navigate_to_the_ti_backoffice_andundisplay_eventmarketselection_that_is_used_in_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and
        DESCRIPTION: **undisplay** Event/Market/Selection that is used in the Timeline Post
        EXPECTED: POST' response should be present with all fields form CMS in WS.
        """
        pass

    def test_003_return_to_the_timeline_and_verify_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify selection for the Timeline Post
        EXPECTED: Changes should be saved successfully in TI (backoffice)Event/Market/Selection is undisplayed
        """
        pass

    def test_004_navigate_to_the_ti_backoffice_anddisplay_eventmarketselection_that_is_used_in_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and
        DESCRIPTION: **display** Event/Market/Selection that is used in Timeline Post
        EXPECTED: 'N/A' should be displayed as greyed out and disabled for the selection for the Post instead of the Price/Odds
        EXPECTED: ->The following attributes are received in Network WS -EIO=&transport=websocket wss://timeline-api-response with type:"POST_CHANGED"
        EXPECTED: should be Displayed: "N"
        """
        pass

    def test_005_refresh_the_page___open_timeline_and_verify_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: Refresh the page -> open 'Timeline' and verify selection for the Timeline Post
        EXPECTED: Changes should be saved successfully in TI (backoffice)Event/Market/Selection is displayed.
        """
        pass

    def test_006_collapse_timeline_and_trigger_undisplaying_eventmarketselection_in_the_ti_backoffice(self):
        """
        DESCRIPTION: **Collapse** 'Timeline' and trigger **undisplaying** Event/Market/Selection in the TI (backoffice)
        EXPECTED: Price/Odds button with available prices should be displayed for the Post
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type:"POST_CHANGED"
        EXPECTED: is Displayed: "Y"
        """
        pass

    def test_007_expand_timeline_and_verify_the_selection_for_the_post_on_ui(self):
        """
        DESCRIPTION: **Expand** 'Timeline' and verify the selection for the Post on UI
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type:"POST_CHANGED"
        EXPECTED: is Displayed: "N"
        EXPECTED: Note:
        EXPECTED: N/A' is displayed as greyed out and disabled for the selection for the Post instead of the Price/Odds
        """
        pass
