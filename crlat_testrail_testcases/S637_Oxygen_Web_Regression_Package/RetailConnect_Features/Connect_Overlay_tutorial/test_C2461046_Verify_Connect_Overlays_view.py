import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2461046_Verify_Connect_Overlays_view(Common):
    """
    TR_ID: C2461046
    NAME: Verify Connect Overlays view
    DESCRIPTION: This test case verifies the view of Connect Overlay
    PRECONDITIONS: Make sure Connect Overlay tutorial feature is turned on in CMS: System configuration -> Connect -> overlay
    PRECONDITIONS: * User need to load SB on mobile device where Connect App and/or RCOMB microsite were used
    PRECONDITIONS: * When Connect App and RCOMB microsite were in use they have written following data into browser storage: cookies: field Name 'CONNECT_TRACKER' = 'false' and in Locale storage: OX.connectOverlayRemain = 4
    PRECONDITIONS: ________________________
    PRECONDITIONS: * To emulate above situation without using Connect App/ RCOMB   open dev tool -> Application tab -> cookies: field Name 'CONNECT_TRACKER' set with 'false' value and in Locale storage: OX.connectOverlayRemain set with value that is more than 0. Reload the SB app
    PRECONDITIONS: * User can be logged in or logged out
    """
    keep_browser_open = True

    def test_001_verify_view_of_connect_overlay(self):
        """
        DESCRIPTION: Verify view of Connect overlay
        EXPECTED: * Black half transparent background
        EXPECTED: * The white close button 'X' (in the top left-hand corner)
        EXPECTED: * An image of the Connect logo (on the header sports ribbon menu)
        EXPECTED: * The arrow on the overlay image is aligned to the Connect logo on the top right (in the header ribbon menu)
        EXPECTED: * 'Scroll right in the menu' text (above the arrow)
        EXPECTED: * 'Bet in-shop & online with Connect' header (in the middle of the page)
        EXPECTED: * 'Collect your winnings instantly in cash and deposit in shop', 'Track and cash out your in-shop bets', 'Get exclusive promotions' texts
        EXPECTED: * Green button 'TAKE ME TO THE CONNECT HUB'
        EXPECTED: * 'Don’t show me this again' link
        """
        pass

    def test_002_verify_connect_overlay_text_corresponds_to_cms_configuration(self):
        """
        DESCRIPTION: Verify Connect overlay text corresponds to CMS Configuration
        EXPECTED: Following text itself and text style correspond to Static Block 'Connect Overlay' (Uri = connect-overlay-en-us):
        EXPECTED: Bet in-shop & online with Connect
        EXPECTED: Collect your winnings instantly in cash and deposit in shop', 'Track and cash out your in-shop bets', 'Get exclusive promotions
        """
        pass
