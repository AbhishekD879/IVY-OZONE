import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870419_Verify_display_Content_of_totepool_markets(Common):
    """
    TR_ID: C44870419
    NAME: "Verify display & Content of totepool markets.
    DESCRIPTION: This TC is to verify the totepool markets.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application.
        EXPECTED: Application is launched and tab is Highlights tab by default.
        """
        pass

    def test_002_navigate_to_any_horse_racing_event_landing_page(self):
        """
        DESCRIPTION: Navigate to any Horse Racing Event landing page.
        EXPECTED: Horse Racing Event landing page is opened.
        """
        pass

    def test_003_click_on_totepool_in_market_selection_bar_and_verify_new_market_sub_header_is_opened_with_marketswinplaceexactatrifectaplacepotquadpotjackpot(self):
        """
        DESCRIPTION: Click on Totepool in Market Selection bar and verify new market sub-header is opened with markets
        DESCRIPTION: win
        DESCRIPTION: Place
        DESCRIPTION: Exacta
        DESCRIPTION: Trifecta
        DESCRIPTION: Placepot
        DESCRIPTION: Quadpot
        DESCRIPTION: Jackpot
        EXPECTED: User is able to see Totepool markets.
        EXPECTED: win
        EXPECTED: Place
        EXPECTED: Exacta
        EXPECTED: Trifecta
        EXPECTED: Placepot
        EXPECTED: Quadpot
        EXPECTED: Jackpot
        EXPECTED: Note:  You may not see Jackpot and Placepot if few of participating events are finished.
        """
        pass

    def test_004_navigate_to_international_totepool_from_a_z_sports_or_scroll_down_on_home_page(self):
        """
        DESCRIPTION: Navigate to international Totepool from A-Z sports or scroll down on home page.
        EXPECTED: International totepool is opened.
        """
        pass

    def test_005_click_on_any_event_and_verify_these_marketswinplaceexactatrifectaplacepotquadpotjackpot(self):
        """
        DESCRIPTION: Click on any event and verify these markets
        DESCRIPTION: win
        DESCRIPTION: Place
        DESCRIPTION: Exacta
        DESCRIPTION: Trifecta
        DESCRIPTION: Placepot
        DESCRIPTION: Quadpot
        DESCRIPTION: Jackpot
        EXPECTED: User is able to
        EXPECTED: win
        EXPECTED: Place
        EXPECTED: Exacta
        EXPECTED: Trifecta
        EXPECTED: Placepot
        EXPECTED: Quadpot
        EXPECTED: Jackpot
        EXPECTED: Note:  You may not see Jackpot and Placepot if few of participating events are finished.
        """
        pass
