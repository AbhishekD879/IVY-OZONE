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
class Test_C59918216_Verify_adding_first_selection_to_Betslip_from_Timeline_and_placed_a_bet(Common):
    """
    TR_ID: C59918216
    NAME: Verify adding first selection to Betslip from Timeline and placed a bet
    DESCRIPTION: Test case verifies adding first selection to Betslip from Timeline
    PRECONDITIONS: "
    PRECONDITIONS: Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 2.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 3.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -Betslip is empty
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: - Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: Post with price is displayed
        """
        pass

    def test_003_tap_on_the_price_button(self):
        """
        DESCRIPTION: Tap on the price button
        EXPECTED: - Quick bet overlay is opened over the top of the timeline
        """
        pass

    def test_004_click_button_add_to_betslip_on_quick_bet_overlay(self):
        """
        DESCRIPTION: Click button 'Add to Betslip' on Quick bet overlay
        EXPECTED: - Quick bet widget is closed
        EXPECTED: - User is returned to timeline
        """
        pass

    def test_005_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: - Selected bet from Timeline is displayed
        """
        pass

    def test_006_enter_stake_and_click_place_bet(self):
        """
        DESCRIPTION: Enter stake and click 'Place Bet'
        EXPECTED: - Bet is placed successfully with the correct date and time
        EXPECTED: - Bet Receipt is displayed
        """
        pass
