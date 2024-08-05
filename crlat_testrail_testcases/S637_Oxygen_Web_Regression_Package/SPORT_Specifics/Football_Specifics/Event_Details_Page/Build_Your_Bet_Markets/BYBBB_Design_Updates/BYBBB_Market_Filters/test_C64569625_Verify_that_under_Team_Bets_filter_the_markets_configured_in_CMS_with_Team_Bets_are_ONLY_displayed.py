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
class Test_C64569625_Verify_that_under_Team_Bets_filter_the_markets_configured_in_CMS_with_Team_Bets_are_ONLY_displayed(Common):
    """
    TR_ID: C64569625
    NAME: Verify that under 'Team Bets' filter the markets configured in CMS with Team Bets are ONLY displayed
    DESCRIPTION: This test case verifies the display of Team Bets tab
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: In CMS &gt; BYB . BYB Markets - Atleast one or more markets should be configured for Team Bets
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: * User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_gt_edp_gt_bet_builder__build_your_bet_tab(self):
        """
        DESCRIPTION: Navigate to Football &gt; EDP &gt; Bet Builder / Build Your Bet tab
        EXPECTED: * Bet Builder / Build Your Bet tab should be displayed
        """
        pass

    def test_003_validate_the_display_of_team_bets_tab(self):
        """
        DESCRIPTION: Validate the display of Team Bets tab
        EXPECTED: * User should be able to click on Team Bets filter
        EXPECTED: * Markets should be displayed under Team Bets
        EXPECTED: * Only those Markets which are configured in CMS with Market type as 'Team Bets'       should be displayed
        """
        pass
