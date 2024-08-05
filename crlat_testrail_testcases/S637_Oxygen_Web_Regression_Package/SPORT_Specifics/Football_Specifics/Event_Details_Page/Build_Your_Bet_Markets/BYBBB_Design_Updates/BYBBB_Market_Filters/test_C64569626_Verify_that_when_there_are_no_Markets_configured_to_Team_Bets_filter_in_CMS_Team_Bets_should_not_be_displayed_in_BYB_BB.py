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
class Test_C64569626_Verify_that_when_there_are_no_Markets_configured_to_Team_Bets_filter_in_CMS_Team_Bets_should_not_be_displayed_in_BYB_BB(Common):
    """
    TR_ID: C64569626
    NAME: Verify that when there are no Markets configured to Team Bets filter in CMS, Team Bets should not be displayed in BYB/BB
    DESCRIPTION: This test case verifies the display of Team Bets filter when there are no Markets configured to Team Bets in CMS
    PRECONDITIONS: 1: No Market in CMS  should be configured to Team Bets (Market Type)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
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
        EXPECTED: * Team Bets filter tab should not be displayed
        """
        pass
