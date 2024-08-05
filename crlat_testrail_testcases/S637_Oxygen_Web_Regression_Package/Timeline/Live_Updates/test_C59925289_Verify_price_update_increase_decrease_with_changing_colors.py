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
class Test_C59925289_Verify_price_update_increase_decrease_with_changing_colors(Common):
    """
    TR_ID: C59925289
    NAME: Verify price update (increase/decrease with changing colors)
    DESCRIPTION: This test case verifies price update (increase/decrease with changing colors)
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 3.Live Campaign is created
    PRECONDITIONS: 4.Timeline posts with prices are created and published
    PRECONDITIONS: 5.Load the app
    PRECONDITIONS: 6.User is logged in ( NOTE Timeline is displayed ONLY for Logged In Users )
    PRECONDITIONS: 7.Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: It should be verified for:
    PRECONDITIONS: Sport / Races
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_click_on_the_timeline_ladbrokes_lounge_button(self):
        """
        DESCRIPTION: Click on the Timeline 'Ladbrokes Lounge' button
        EXPECTED: Page with the published post should be opened
        EXPECTED: ->Price should be present in the post
        EXPECTED: ->Content should be same as in CMS
        EXPECTED: ->In WS 'POST' response should be present with all fields form CMS
        """
        pass

    def test_002_go_to_ob_and_change_the_price_for_the_event(self):
        """
        DESCRIPTION: Go to OB and change the price for the event
        EXPECTED: Changes should be saved successfully in OB
        EXPECTED: ->Price for the event should be changed.
        """
        pass

    def test_003___return_to_the_timeline_and_verify_outcomes_for_the_event__check_ws(self):
        """
        DESCRIPTION: - Return to the 'Timeline' and verify outcomes for the event
        DESCRIPTION: - Check WS
        EXPECTED: 3.Corresponding 'Price/Odds' button immediately displays the new price and for a few seconds it changes its color to:
        EXPECTED: ->Blue color if the price has decreased
        EXPECTED: ->Red color if the price has increased
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type "POST_CHANGED":
        EXPECTED: selectionEvent:
        EXPECTED: obEvent:
        EXPECTED: prices:
        EXPECTED: priceDen: "X"
        EXPECTED: priceNum: "Y"
        """
        pass

    def test_004_collapse_timeline_and_trigger_price_change_for_the_event(self):
        """
        DESCRIPTION: **Collapse** 'Timeline' and trigger price change for the event
        EXPECTED: The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type "POST_CHANGED":
        EXPECTED: selectionEvent:
        EXPECTED: obEvent:
        EXPECTED: prices:
        EXPECTED: priceDen: "X"
        EXPECTED: priceNum: "Y"
        """
        pass

    def test_005_expand_timeline_and_verify_price_change_for_the_event_on_ui(self):
        """
        DESCRIPTION: **Expand** 'Timeline' and verify price change for the event on UI
        EXPECTED: Corresponding 'Price/Odds' button immediately displays the new price and for a few seconds it changes its color to:
        EXPECTED: ->Blue color if the price has decreased
        EXPECTED: ->Red color if the price has increased
        """
        pass
