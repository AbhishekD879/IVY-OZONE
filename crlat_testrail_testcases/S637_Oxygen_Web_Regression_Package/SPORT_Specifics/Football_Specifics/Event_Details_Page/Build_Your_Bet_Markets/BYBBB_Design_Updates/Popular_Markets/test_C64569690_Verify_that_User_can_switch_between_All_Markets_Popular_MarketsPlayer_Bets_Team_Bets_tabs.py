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
class Test_C64569690_Verify_that_User_can_switch_between_All_Markets_Popular_MarketsPlayer_Bets_Team_Bets_tabs(Common):
    """
    TR_ID: C64569690
    NAME: Verify that User can switch between All Markets, Popular Markets,Player Bets, Team Bets tabs
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral Application
        EXPECTED: User should be able to Launch the Ladbrokes/Coral successfully
        """
        pass

    def test_002_navigate_to_any_event_which_has_byb_markets_gt_edp(self):
        """
        DESCRIPTION: Navigate to ANY event which has BYB markets &gt; EDP
        EXPECTED: User should be able to navigate to Football Event Details page
        """
        pass

    def test_003_click_on_build_your_bet_or_bet_builder(self):
        """
        DESCRIPTION: Click on Build Your Bet or Bet Builder
        EXPECTED: * Bet Builder/Build Your Bet tab should be opened
        """
        pass

    def test_004_validate_the_display_of_bybbb_tab(self):
        """
        DESCRIPTION: Validate the display of BYB/BB tab
        EXPECTED: * Four Filters should be displayed based on the CMS configuration
        EXPECTED: * All Markets should be selected by default
        """
        pass

    def test_005_switch_between_the_tabs_for_all_markets_popular_marketsplayer_bets_team_bets_tabs(self):
        """
        DESCRIPTION: Switch between the tabs for All Markets, Popular Markets,Player Bets, Team Bets tabs
        EXPECTED: * Selected tab should be displayed
        """
        pass

    def test_006_validate_the_display_of_selected__tab(self):
        """
        DESCRIPTION: Validate the display of selected  tab
        EXPECTED: * Selected tab should be selected and highlighted
        EXPECTED: * Highlights should be as per Zeplin
        """
        pass

    def test_007_validate_the_display_order_of_the_markets_for_selected_taball_markets_popular_marketsplayer_bets_team_bets_tabs(self):
        """
        DESCRIPTION: Validate the display order of the markets for selected tab(All Markets, Popular Markets,Player Bets, Team Bets tabs)
        EXPECTED: * The display order of Markets should be as per CMS
        """
        pass

    def test_008_validate_the_markets_expanded_by_default(self):
        """
        DESCRIPTION: Validate the markets expanded by default
        EXPECTED: * First Market should be expanded by default
        """
        pass
