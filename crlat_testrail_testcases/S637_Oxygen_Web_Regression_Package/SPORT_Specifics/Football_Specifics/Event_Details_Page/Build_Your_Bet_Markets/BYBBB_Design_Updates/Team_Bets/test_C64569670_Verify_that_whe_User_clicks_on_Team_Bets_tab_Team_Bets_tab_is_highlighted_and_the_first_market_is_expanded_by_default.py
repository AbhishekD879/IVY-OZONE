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
class Test_C64569670_Verify_that_whe_User_clicks_on_Team_Bets_tab_Team_Bets_tab_is_highlighted_and_the_first_market_is_expanded_by_default(Common):
    """
    TR_ID: C64569670
    NAME: Verify that whe User clicks on Team Bets tab , Team Bets tab is highlighted and the first market is expanded by default
    DESCRIPTION: 
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
        EXPECTED: User should be navigated to Football EDP
        """
        pass

    def test_003_click_on_build_your_betbet_builder_tab(self):
        """
        DESCRIPTION: Click on Build Your Bet/Bet Builder tab
        EXPECTED: * BYB/BB tab should be opened
        EXPECTED: * Filters should be displayed as per the CMS configurations
        EXPECTED: * All Markets should be selected by default
        """
        pass

    def test_004_click_on_team_bets_and_validate_the_display_of_team_bets(self):
        """
        DESCRIPTION: Click on Team Bets and Validate the display of Team Bets
        EXPECTED: * Team Bets filter should be displayed
        EXPECTED: * Team Bets should be highlighted
        EXPECTED: * By default first Market should be Expanded
        """
        pass

    def test_005_validate_the_display_order_of_markets(self):
        """
        DESCRIPTION: Validate the display order of Markets
        EXPECTED: * Markets should be displayed as per CMS order
        """
        pass

    def test_006_expand__collapse_and_validate(self):
        """
        DESCRIPTION: Expand / Collapse and Validate
        EXPECTED: User should be able to Expand / Collapse the Markets
        """
        pass

    def test_007_in_cms_unselect_team_bets_market_type_for_any_of_team_bet_marketvalidate_the_display_of_that_market_in_team_bets(self):
        """
        DESCRIPTION: In CMS unselect Team Bets Market Type for any of Team Bet Market
        DESCRIPTION: Validate the display of that Market in Team Bets
        EXPECTED: * That Market should no longer be displayed under Team Bets Filter
        EXPECTED: * That Market should be displayed in All Markets filter
        """
        pass

    def test_008_in_cms___no_market_should_be_configured_with_team_bets_as_market_typevalidate_the_display_of_team_bets_filter(self):
        """
        DESCRIPTION: In CMS - No Market should be configured with Team Bets as Market Type
        DESCRIPTION: Validate the display of Team Bets filter
        EXPECTED: Team Bets Filter should no longer be displayed
        """
        pass
