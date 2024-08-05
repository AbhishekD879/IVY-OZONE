import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569675_Verify_on_toggle_between_the_different_filters_it_should_be_GA_tag(Common):
    """
    TR_ID: C64569675
    NAME: Verify on toggle between the different filters it should be GA tag
    DESCRIPTION: This test case verify the the toggle betweeen the filters
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: * User should be navigated to EDP
        EXPECTED: * Build Your Bet /Bet Builder tab should be displayed
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: * BYB/BB tab should be displayed
        EXPECTED: * Filters should be displayed
        EXPECTED: * All Markets tab should be displayed by default
        """
        pass

    def test_004_validate_toggle_between_the_filters_all_marketspopular_marketsplayer_betsteam_bets_is_ga_tracking_in_console(self):
        """
        DESCRIPTION: Validate toggle between the filters (All Markets,Popular markets,Player bets,team bets) is Ga Tracking in console
        EXPECTED: Toggle between the filters (All Markets,Popular markets,Player bets,team bets) should be Ga Tracked
        EXPECTED: ![](index.php?/attachments/get/4a4b97b8-274e-480e-a69a-84c5e480277b)
        """
        pass
