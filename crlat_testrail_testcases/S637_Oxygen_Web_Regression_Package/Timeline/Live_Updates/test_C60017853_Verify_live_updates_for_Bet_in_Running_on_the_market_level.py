import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@vtest
class Test_C60017853_Verify_live_updates_for_Bet_in_Running_on_the_market_level(Common):
    """
    TR_ID: C60017853
    NAME: Verify  live updates for 'Bet in Running' on the market level
    DESCRIPTION: This test case verifies live updates for 'Bet in Running' on the market level
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: -Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: -Bet in Running' should work only for live events
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: Sport/Races
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_click_on_the_timeline_bubblealadbrokes_ladbrokes_lounge_buttonbcoral_coral_pulse_button(self):
        """
        DESCRIPTION: Click on the Timeline Bubble
        DESCRIPTION: a.Ladbrokes-'Ladbrokes Lounge' button
        DESCRIPTION: b.Coral-'Coral Pulse' button
        EXPECTED: Page with the published post should be opened
        EXPECTED: Price should be present in the post
        EXPECTED: Content should be the same as in CMS
        EXPECTED: In WS 'POST' response should be present with all fields form CMS
        """
        pass

    def test_002_go_to_ob_and_uncheck_the_bet_in_running_checkbox_on_the_market_level(self):
        """
        DESCRIPTION: Go to OB and uncheck the 'Bet in Running' checkbox on the market level
        EXPECTED: Changes are saved successfully in TI
        """
        pass

    def test_003_return_to_the_timeline_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify outcomes for the event
        EXPECTED: - Corresponding 'Price/Odds' button displays with n/a status on UI
        EXPECTED: ![](index.php?/attachments/get/119657446)
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type: POST_CHANGED
        EXPECTED: isMarketBetInRun: f
        """
        pass

    def test_004_go_to_ob_and_check_the_bet_in_running_checkbox_on_the_market_level(self):
        """
        DESCRIPTION: Go to OB and check the 'Bet in Running' checkbox on the market level
        EXPECTED: Changes are saved successfully in TI
        """
        pass

    def test_005_return_to_the_timeline_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify outcomes for the event
        EXPECTED: - Price/Odds button of this event is displayed near post
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type: POST_CHANGED
        EXPECTED: isMarketBetInRun: true
        """
        pass
