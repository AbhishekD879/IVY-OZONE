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
class Test_C64569663_Verify_that_Flag_crest_is_displayed_as_configured_in_CMS_Asset_Manager(Common):
    """
    TR_ID: C64569663
    NAME: Verify that Flag/crest is displayed as configured in CMS Asset Manager
    DESCRIPTION: Verify that Flag/crest is displayed as configured in CMS Asset Manager
    PRECONDITIONS: Configure Flag/Crest in CMS Asset Manager
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
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_validate_the_display_of_player_bets(self):
        """
        DESCRIPTION: Validate the display of Player Bets
        EXPECTED: * Player Bets should no longer be displayed in dropdown view
        EXPECTED: * Player Bets should be displayed in their own accordions
        EXPECTED: * Player Total Assists
        EXPECTED: * Player Total Passes
        EXPECTED: * Player Total Shots
        EXPECTED: * Player Total Shots on Target
        EXPECTED: * Player Total Tackles
        EXPECTED: * Player Shots Outside the box
        EXPECTED: * Offside
        EXPECTED: * Player Total Goals
        EXPECTED: * Goals Inside the box
        EXPECTED: * Goals Outside the box
        """
        pass

    def test_005_expand_any_player_market_mentioned_in_the_above_step_and_validate_the_display_of_player_names(self):
        """
        DESCRIPTION: Expand any Player Market mentioned in the above step and Validate the display of Player names
        EXPECTED: Crest/Flag should be displayed before the player name which configured in Asset Manager CMS
        """
        pass

    def test_006_expand_and_collapse_the_player_market_and_verify_crestflag(self):
        """
        DESCRIPTION: Expand and Collapse the player market and verify Crest/Flag
        EXPECTED: Crest/Flag should be displayed constantly before the player name which configured in Asset Manager CMS
        """
        pass
