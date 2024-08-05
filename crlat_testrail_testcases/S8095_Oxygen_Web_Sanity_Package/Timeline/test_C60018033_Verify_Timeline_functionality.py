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
class Test_C60018033_Verify_Timeline_functionality(Common):
    """
    TR_ID: C60018033
    NAME: Verify Timeline functionality
    DESCRIPTION: This test case verifies Timeline functionality
    PRECONDITIONS: - Confluence instruction - **How to create Timeline Template, Campaign, Posts** - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: - Design - https://app.zeplin.io/project/5dc59d1d83c70b83632e749c/screen/5efc4d09b9928c4174416bf9
    PRECONDITIONS: _________________________________
    PRECONDITIONS: - Timeline/Splash Page should be Turn ON in the CMS
    PRECONDITIONS: - LIVE Campaign with Posts are configured in the CMS
    PRECONDITIONS: - User haven't seen Splash page (OX.timelineTutorialOverlay is missed in the local storage)
    PRECONDITIONS: Load the app
    PRECONDITIONS: Log in to the app
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline(self):
        """
        DESCRIPTION: Navigate to the page with configured Timeline
        EXPECTED: - The tutorial Splash page will be displayed at the end of the existing pop-up sequence
        EXPECTED: - Header styled as per design and content as configured in CMS:
        EXPECTED: - Phone svg icon
        EXPECTED: - Arrow svg icons (configured in CMS)
        EXPECTED: - Text bubbles
        EXPECTED: - Option to select 'X'
        EXPECTED: - Options to select 'OK THANKS' cta
        """
        pass

    def test_002_click_on_the_x_or_ok_thanks_button(self):
        """
        DESCRIPTION: Click on the 'X' or 'OK, THANKS!' button
        EXPECTED: - Splash page is closed
        """
        pass

    def test_003_tap_on_the_timeline_header_ladbrokes_lounge(self):
        """
        DESCRIPTION: Tap on the Timeline header 'LADBROKES LOUNGE'
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - The following attributes are displayed in the Timeline header:
        EXPECTED: - 'LADBROKES LOUNGE' text on the left side of the header
        EXPECTED: - 'Minimise' text on the right side of the header
        EXPECTED: - Configured Posts/Posts with selection are displayed in the Timeline
        """
        pass

    def test_004_tap_on_the_minimise_text(self):
        """
        DESCRIPTION: Tap on the 'Minimise' text
        EXPECTED: - Timeline returns to the collapsed position
        """
        pass

    def test_005_tap_on_the_timeline_header_ladbrokes_lounge_again(self):
        """
        DESCRIPTION: Tap on the Timeline header 'LADBROKES LOUNGE' again
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - Configured Posts with selections (price buttons) are displayed in the Timeline
        """
        pass

    def test_006_tap_on_the_price_button_for_the_post(self):
        """
        DESCRIPTION: Tap on the price button for the Post
        EXPECTED: - Quick bet overlay is opened over the top of the timeline
        """
        pass

    def test_007_enter_stake_and_click_place_bet(self):
        """
        DESCRIPTION: Enter stake and click 'Place Bet'
        EXPECTED: - Bet is placed successfully with correct date and time
        EXPECTED: - Bet Receipt is displayed
        """
        pass

    def test_008_close_bet_receipt(self):
        """
        DESCRIPTION: Close 'Bet Receipt'
        EXPECTED: - 'Bet Receipt' is closed
        EXPECTED: - Expanded Timeline is displayed
        """
        pass

    def test_009_tap_on_the_price_button_again(self):
        """
        DESCRIPTION: Tap on the price button again
        EXPECTED: Quick bet overlay is opened over the top of the timeline
        """
        pass

    def test_010_click_button_add_to_betslip_on_quick_bet_overlay(self):
        """
        DESCRIPTION: Click button 'Add to Betslip' on Quick bet overlay
        EXPECTED: - Quick bet widget is closed
        EXPECTED: - User is returned to timeline
        """
        pass

    def test_011_navigate_to_betslipenter_stake_and_click_place_bet(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Enter stake and click 'Place Bet'
        EXPECTED: - Selected bet from Timeline is displayed in the Betslip
        EXPECTED: - Bet is placed successfully with the correct date and time
        EXPECTED: - Bet Receipt is displayed
        """
        pass
