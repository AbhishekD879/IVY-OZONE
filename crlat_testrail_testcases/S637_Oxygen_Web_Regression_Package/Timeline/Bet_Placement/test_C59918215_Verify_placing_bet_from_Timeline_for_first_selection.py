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
class Test_C59918215_Verify_placing_bet_from_Timeline_for_first_selection(Common):
    """
    TR_ID: C59918215
    NAME: Verify placing bet from Timeline for first selection
    DESCRIPTION: This test case verifies placing bet from Timeline for the first selection
    PRECONDITIONS: "
    PRECONDITIONS: Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts (TBD)
    PRECONDITIONS: 1.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 2.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 3.Timeline posts with prices are created and published
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -User Balance is positive
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
        EXPECTED: - Post with price is displayed
        """
        pass

    def test_003_tap_on_the_price_button(self):
        """
        DESCRIPTION: Tap on the price button
        EXPECTED: - Quick bet overlay is opened over the top of the timeline
        """
        pass

    def test_004_enter_stake_and_click_place_bet(self):
        """
        DESCRIPTION: Enter stake and click 'Place Bet'
        EXPECTED: - Bet is placed successfully with correct date and time
        EXPECTED: - Bet Receipt is displayed
        """
        pass

    def test_005_close_bet_receipt(self):
        """
        DESCRIPTION: Close 'Bet Receipt'
        EXPECTED: - 'Bet Receipt' is closed
        EXPECTED: - Expanded Timeline is displayed
        """
        pass
