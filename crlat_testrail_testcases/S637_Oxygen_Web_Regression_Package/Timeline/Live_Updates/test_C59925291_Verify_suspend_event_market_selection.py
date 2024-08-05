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
class Test_C59925291_Verify_suspend_event_market_selection(Common):
    """
    TR_ID: C59925291
    NAME: Verify suspend event/market/selection
    DESCRIPTION: This test case verifies suspend event/market/selection
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Camping is created
    PRECONDITIONS: 2.Timeline posts with prices are created and published
    PRECONDITIONS: 3.Load the app
    PRECONDITIONS: 4.User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: 5.Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: Sport / Races
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_click_on_the_timeline_bubblea_ladbrokes_lounge_buttonb_coral_pulse_button(self):
        """
        DESCRIPTION: Click on the Timeline Bubble
        DESCRIPTION: a. 'Ladbrokes Lounge' button.
        DESCRIPTION: b. 'Coral Pulse' button.
        EXPECTED: Page with the published post should be opened
        EXPECTED: ->Price should be present in the post
        EXPECTED: ->Content should be the same as in CMS
        EXPECTED: ->In WS 'POST' response should be present with all fields form CMS
        """
        pass

    def test_002_go_to_ob_and_suspend_an_event(self):
        """
        DESCRIPTION: Go to OB and **Suspend** an event
        EXPECTED: Changes should be saved successfully in TI
        EXPECTED: ->Event should be suspended
        """
        pass

    def test_003_return_to_the_timeline_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify outcomes for the event
        EXPECTED: Price/Odds button of this event should be displayed immediately as greyed out and becomes disabled
        EXPECTED: The following attributes should be received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type:"POST_CHANGED"
        EXPECTED: selectionEvent:
        EXPECTED: obEvent:
        EXPECTED: isActive: false
        EXPECTED: eventStatusCode: "S"
        """
        pass

    def test_004_go_to_ob_and_do_active_an_event(self):
        """
        DESCRIPTION: Go to OB and do **Active** an event
        EXPECTED: Price/Odds button of this event is no more disabled, it becomes active immediately and displays the price
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type:"POST_CHANGED" selectionEvent: obEvent:
        EXPECTED: isActive: true
        EXPECTED: eventStatusCode: "A"
        """
        pass

    def test_005_collapse_timeline_and_trigger_suspension_for_the_event(self):
        """
        DESCRIPTION: **Collapse** 'Timeline' and trigger suspension for the event
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type:"POST_CHANGED" selectionEvent: obEvent:
        EXPECTED: isActive: false
        EXPECTED: eventStatusCode: "S"
        """
        pass

    def test_006_expand_timeline__and_verify_event_suspension_on_ui(self):
        """
        DESCRIPTION: **Expand** 'Timeline'  and verify event suspension on UI
        EXPECTED: Event suspension update is received
        EXPECTED: Price/Odds button of this event is displayed immediately as greyed out and becomes disabled
        """
        pass

    def test_007_repeat_steps_2_6_for_suspension_on_the_marketoutcome_leveltypepost_changed___status_atypepost_changed___status_s(self):
        """
        DESCRIPTION: Repeat steps 2-6 for **Suspension on the Market/Outcome level:**
        DESCRIPTION: "type":"POST_CHANGED" - status: "A"
        DESCRIPTION: "type":"POST_CHANGED" - status: "S"
        EXPECTED: 
        """
        pass
