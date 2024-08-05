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
class Test_C59918217_Verify_adding_subsequent_selections_to_Betslip_from_Timeline(Common):
    """
    TR_ID: C59918217
    NAME: Verify adding subsequent selections to Betslip from Timeline
    DESCRIPTION: Test case verifies adding subsequent selections to Betslip from Timeline or previously added bets
    PRECONDITIONS: "Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 4.Timeline posts with prices is created and published
    PRECONDITIONS: Zeplin Design -
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -Several Bets are already added to Betslip
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
        EXPECTED: - Green 'selected' state  is applied in timeline for that selection
        EXPECTED: - Selection is added to Betslip
        EXPECTED: - Betslip counter is increased by one
        EXPECTED: - Expanded Timeline is still displaying
        """
        pass

    def test_004_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: - Selected bet from Timeline is present on Betslip
        """
        pass

    def test_005_remove_bet_that_was_added_from_timeline_andnavigate_again_to_timeline(self):
        """
        DESCRIPTION: Remove bet that was added from Timeline and
        DESCRIPTION: navigate again to Timeline
        EXPECTED: - 'Selected' state isn't green anymore, it is displayed as an unchecked selection
        """
        pass
